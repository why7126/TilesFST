from unittest.mock import Mock
import pytest
from app.modules.media.cos_upload import TencentCOSUploadGateway, UploadObjectMismatch, ConfirmedObject, part_length

@pytest.fixture
def client():return Mock()

@pytest.fixture
def gateway(client):return TencentCOSUploadGateway(client,bucket='test-bucket',region='test-region')


def test_authorization_binds_exact_part_and_length(client,gateway):
    gateway.authorize('tmp/test.bin',length=1024,expires=900,upload_id='upload',part_number=2)
    kw=client.get_presigned_url.call_args.kwargs
    assert kw['Method']=='PUT' and kw['Params']=={'uploadId':'upload','partNumber':2}
    assert kw['Headers']=={'Content-Length':'1024'}
    assert 'SecretKey' not in kw

@pytest.mark.parametrize('number',[0,4,10001])
def test_part_bounds(number):
    with pytest.raises(UploadObjectMismatch):part_length(8388608*2+1,8388608,number)


def test_last_part_length():assert part_length(8388609,8388608,2)==1

@pytest.mark.parametrize('parts',[
    [{'PartNumber':1,'Size':1048576,'ETag':'one'}],
    [{'PartNumber':1,'Size':1048576,'ETag':'one'},{'PartNumber':2,'Size':5,'ETag':'two'}],
    [{'PartNumber':1,'Size':1048576,'ETag':'one'},{'PartNumber':1,'Size':4,'ETag':'two'}],
])
def test_complete_rejects_missing_oversized_duplicate_parts(client,gateway,parts):
    client.list_parts.return_value={'Part':parts,'IsTruncated':'false'}
    with pytest.raises(UploadObjectMismatch):gateway.complete('tmp/test','upload',expected_size=1048580,part_size=1048576)
    client.complete_multipart_upload.assert_not_called()


def test_complete_uses_server_parts_and_exact_version(client,gateway):
    client.list_parts.return_value={'Part':[{'PartNumber':1,'Size':1048576,'ETag':'one'},{'PartNumber':2,'Size':4,'ETag':'two'}]}
    client.complete_multipart_upload.return_value={'x-cos-version-id':'source-version'}
    client.head_object.return_value={'Content-Length':'1048580','ETag':'combined','x-cos-version-id':'source-version'}
    result=gateway.complete('tmp/test','upload',expected_size=1048580,part_size=1048576)
    assert result.version_id=='source-version'
    assert client.head_object.call_args.kwargs['VersionId']=='source-version'


def test_copy_freezes_source_version_and_checks_target(client,gateway):
    client.copy_object.return_value={'VersionId':'target-version', 'x-cos-copy-source-version-id':'source-version'}
    client.head_object.return_value={'Content-Length':'4','ETag':'copy','x-cos-version-id':'target-version'}
    result=gateway.copy_stable(ConfirmedObject('tmp/test','source-version','etag',4,'video/mp4'),'videos/test')
    assert result.version_id=='target-version'
    assert client.copy_object.call_args.kwargs['CopySource']['VersionId']=='source-version'
    assert client.copy_object.call_args.kwargs['CopySourceIfMatch']=='etag'


def test_version_protection_required(client,gateway):
    client.get_bucket_versioning.return_value={}
    with pytest.raises(UploadObjectMismatch):gateway.initiate('tmp/test','video/mp4')
    client.create_multipart_upload.assert_not_called()


def test_cleanup_never_deletes_latest_implicitly(client,gateway):
    with pytest.raises(UploadObjectMismatch):gateway.delete_version('tmp/test','')
    client.delete_object.assert_not_called()
    gateway.delete_version('tmp/test','known-version')
    assert client.delete_object.call_args.kwargs['VersionId']=='known-version'


def test_lost_multipart_completion_response_recovers_only_existing_version(client, gateway):
    class MissingUpload(Exception):
        def get_error_code(self): return 'NoSuchUpload'
    client.list_parts.side_effect = MissingUpload()
    client.head_object.return_value = {'Content-Length': '1048580', 'ETag': 'combined', 'x-cos-version-id': 'completed-version'}
    result = gateway.complete('tmp/test', 'upload', expected_size=1048580, part_size=1048576)
    assert result.version_id == 'completed-version'
    client.complete_multipart_upload.assert_not_called()
    client.head_object.side_effect = RuntimeError('object not found')
    from app.core.exceptions import AppError
    with pytest.raises(AppError): gateway.complete('tmp/test', 'upload', expected_size=1048580, part_size=1048576)


def test_cleanup_enumeration_excludes_neighbor_keys_and_keeps_version_ids(client, gateway):
    client.list_objects_versions.return_value = {'Version':[{'Key':'tmp/one','VersionId':'v1'},{'Key':'tmp/one-neighbor','VersionId':'v2'}], 'DeleteMarker':[{'Key':'tmp/one','VersionId':'marker'}]}
    assert list(gateway.versions('tmp/one')) == ['v1','marker']
    client.list_multipart_uploads.return_value = {'Upload':[{'Key':'tmp/one','UploadId':'one'},{'Key':'tmp/one-neighbor','UploadId':'neighbor'}]}
    assert list(gateway.multipart_uploads('tmp/one')) == ['one']


def test_copy_integrity_rejects_different_crc64(client, gateway):
    client.copy_object.return_value = {'VersionId':'copy-version'}
    client.head_object.return_value = {'Content-Length':'4','ETag':'copy','x-cos-version-id':'copy-version','x-cos-hash-crc64ecma':'wrong'}
    with pytest.raises(UploadObjectMismatch):
        gateway.copy_stable(ConfirmedObject('tmp/test','source-version','etag',4,'video/mp4','expected'), 'videos/test')

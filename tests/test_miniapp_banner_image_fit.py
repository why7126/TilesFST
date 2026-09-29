"""REQ-0137: image containment must not change media routing or video behavior."""
from pathlib import Path
import re

import pytest

MINIAPP = Path(__file__).resolve().parents[1] / "src" / "miniapp"


def read(path):
    return (MINIAPP / path).read_text(encoding="utf-8")


def tags(page, tag, css_class):
    return [node for node in re.findall(rf'<{tag}\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*>' , read(f"pages/{page}/index.wxml"))
            if f'class="{css_class}"' in node]


@pytest.mark.parametrize("page,css_class", [("index", "hero-image"), ("brand-list", "brand-hero-image")])
def test_banner_display_and_thumbnail_both_contain_image(page, css_class):
    nodes = tags(page, "authorized-image", css_class)
    assert len(nodes) == 2
    for node, field, branch in zip(nodes, ["display_url", "thumbnail_url"], ["if", "elif"]):
        assert 'mode="aspectFit"' in node
        assert f'wx:{branch}="{{{{item.{field}}}}}"' in node
        assert f'src="{{{{item.{field}}}}}"' in node
        assert 'resource-type="banner_image"' in node
        assert 'resource-id="{{item.id}}"' in node
        if page == "brand-list":
            assert 'lazy-load="{{index > 0}}"' in node
            assert 'binderror="onImageError"' in node
    markup = read(f"pages/{page}/index.wxml")
    assert 'bindtap="openBanner"' in markup
    assert f'<view wx:else class="{css_class.replace("image", "copy")}">' in markup


def test_gallery_containment_is_image_only_and_preserves_original_preview():
    image, = tags("tile-detail", "authorized-image", "gallery-image")
    assert 'wx:if="{{item.media_type == \'image\'}}"' in image
    assert 'mode="aspectFit"' in image
    assert 'src="{{item.display_url || item.thumbnail_url || imageFallback}}"' in image
    assert 'data-url="{{item.original_url || item.preview_url || item.url || item.display_url}}"' in image
    assert 'bindtap="previewImage"' in image
    assert 'lazy-load="{{index > 0}}"' in image
    video, = tags("tile-detail", "video", "gallery-image")
    assert 'object-fit="cover"' in video
    assert 'poster="{{item.cover_url || product.cover_image || \'\'}}"' in video
    assert 'bindplay="onVideoPlay"' in video
    assert 'bindpause="onVideoPause"' in video
    assert 'mode=' not in video
    assert all('mode="aspectFill"' in node for node in tags("tile-detail", "authorized-image", "recommend-image"))


def test_authorized_image_forwards_fit_during_signed_url_rendering():
    component = read("components/authorized-image/index.wxml")
    assert 'mode="{{mode}}"' in component
    assert 'src="{{signedUrl}}"' in component
    assert 'binderror="onImageError"' in component
    assert 'bindload="onImageLoad"' in component

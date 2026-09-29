import { AuthorizedImage } from '@/features/media/authorized-media';
import type { MediaReadReference } from '@/shared/api/generated';
import { useEffect, useMemo, useState } from 'react';

type FallbackListImageProps = {
  reference?: MediaReadReference;
  thumbnailUrl?: string | null;
  displayUrl?: string | null;
  originalUrl?: string | null;
  alt?: string;
};

export function FallbackListImage({
  reference,
  thumbnailUrl,
  displayUrl,
  originalUrl,
  alt = '',
}: FallbackListImageProps) {
  const sources = useMemo(
    () =>
      [thumbnailUrl, displayUrl, originalUrl]
        .filter((src): src is string => Boolean(src))
        .filter((src, index, all) => all.indexOf(src) === index),
    [thumbnailUrl, displayUrl, originalUrl],
  );
  const sourceKey = sources.join('\0');
  const [sourceIndex, setSourceIndex] = useState(0);

  useEffect(() => {
    setSourceIndex(0);
  }, [sourceKey]);

  const src = sources[sourceIndex];
  if (reference) return <AuthorizedImage reference={reference} src={src} alt={alt} />;
  if (!src) return null;

  return <img src={src} alt={alt} onError={() => setSourceIndex((index) => index + 1)} />;
}

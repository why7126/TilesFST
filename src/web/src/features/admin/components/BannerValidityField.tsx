const HOURS = Array.from({ length: 24 }, (_, index) => String(index).padStart(2, '0'));
const MINUTES = Array.from({ length: 60 }, (_, index) => String(index).padStart(2, '0'));

interface Segment {
  date: string;
  hour: string;
  minute: string;
}

function parseSegment(value: string): Segment {
  if (!value) {
    return { date: '', hour: '00', minute: '00' };
  }
  const match = value.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})/);
  if (!match) {
    return { date: '', hour: '00', minute: '00' };
  }
  return { date: match[1], hour: match[2], minute: match[3] };
}

function buildSegment(segment: Segment): string {
  if (!segment.date) return '';
  return `${segment.date}T${segment.hour}:${segment.minute}`;
}

interface BannerValidityFieldProps {
  validFrom: string;
  validTo: string;
  onValidFromChange: (value: string) => void;
  onValidToChange: (value: string) => void;
}

function SegmentControls({
  segment,
  onChange,
}: {
  segment: Segment;
  onChange: (next: Segment) => void;
}) {
  return (
    <div className="banner-validity-segment">
      <input
        type="date"
        className="input banner-validity-date"
        value={segment.date}
        onChange={(event) => onChange({ ...segment, date: event.target.value })}
      />
      <select
        className="select banner-validity-time"
        value={segment.hour}
        aria-label="小时"
        onChange={(event) => onChange({ ...segment, hour: event.target.value })}
      >
        {HOURS.map((hour) => (
          <option key={hour} value={hour}>
            {hour}
          </option>
        ))}
      </select>
      <span className="banner-validity-colon">:</span>
      <select
        className="select banner-validity-time"
        value={segment.minute}
        aria-label="分钟"
        onChange={(event) => onChange({ ...segment, minute: event.target.value })}
      >
        {MINUTES.map((minute) => (
          <option key={minute} value={minute}>
            {minute}
          </option>
        ))}
      </select>
    </div>
  );
}

export function BannerValidityField({
  validFrom,
  validTo,
  onValidFromChange,
  onValidToChange,
}: BannerValidityFieldProps) {
  const fromSegment = parseSegment(validFrom);
  const toSegment = parseSegment(validTo);

  return (
    <div className="banner-validity-field">
      <SegmentControls
        segment={fromSegment}
        onChange={(next) => onValidFromChange(buildSegment(next))}
      />
      <span className="banner-validity-separator">至</span>
      <SegmentControls
        segment={toSegment}
        onChange={(next) => onValidToChange(buildSegment(next))}
      />
    </div>
  );
}

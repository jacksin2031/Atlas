import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import { TemplateImageEditor } from '../../components/inspector/property-inspector';

describe('TemplateImageEditor', () => {
  it('offers an image picker when no template is selected', () => {
    const markup = renderToStaticMarkup(
      <TemplateImageEditor value="" fileName="" onCommit={() => undefined} />,
    );

    expect(markup).toContain('No image selected');
    expect(markup).toContain('Choose image');
    expect(markup).toContain('accept="image/png,image/jpeg,.png,.jpg,.jpeg"');
  });

  it('shows the selected template preview and replacement controls', () => {
    const markup = renderToStaticMarkup(
      <TemplateImageEditor
        value="data:image/png;base64,dGVzdA=="
        fileName="target.png"
        onCommit={() => undefined}
      />,
    );

    expect(markup).toContain('alt="Template preview"');
    expect(markup).toContain('target.png');
    expect(markup).toContain('Replace image');
    expect(markup).toContain('Clear');
  });
});

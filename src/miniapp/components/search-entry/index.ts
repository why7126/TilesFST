Component({
  properties: {
    keyword: { type: String, value: '' },
    placeholder: { type: String, value: '搜索瓷砖名称、编号或规格' },
    scope: { type: String, value: 'all' },
    sourcePage: { type: String, value: 'unknown' },
    disabled: { type: Boolean, value: false },
    showBack: { type: Boolean, value: false },
    mode: { type: String, value: 'input' },
  },

  methods: {
    onEntryTap() {
      if (this.data.disabled || this.data.mode !== 'entry') return;
      this.triggerEvent('tapentry', {
        keyword: this.data.keyword,
        scope: this.data.scope,
        sourcePage: this.data.sourcePage,
      });
    },

    onInput(event: WechatMiniprogram.Input) {
      this.triggerEvent('input', {
        keyword: event.detail.value,
        scope: this.data.scope,
        sourcePage: this.data.sourcePage,
      });
    },

    onSubmit(event?: WechatMiniprogram.Input) {
      const keyword = event?.detail?.value || this.data.keyword;
      if (this.data.disabled) return;
      this.triggerEvent('submit', {
        keyword,
        scope: this.data.scope,
        sourcePage: this.data.sourcePage,
      });
    },

    onClear() {
      this.triggerEvent('clear', {
        scope: this.data.scope,
        sourcePage: this.data.sourcePage,
      });
    },

    onCancel() {
      this.triggerEvent('cancel', {
        scope: this.data.scope,
        sourcePage: this.data.sourcePage,
      });
    },
  },
});

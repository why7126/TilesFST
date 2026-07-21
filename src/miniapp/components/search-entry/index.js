Component({
  properties: {
    keyword: { type: String, value: '' },
    placeholder: { type: String, value: '搜索瓷砖名称、编号或规格' },
    scope: { type: String, value: 'all' },
    sourcePage: { type: String, value: 'unknown' },
    disabled: { type: Boolean, value: false },
    showBack: { type: Boolean, value: false },
  },

  methods: {
    onInput(event) {
      this.triggerEvent('input', {
        keyword: event.detail.value,
        scope: this.data.scope,
        sourcePage: this.data.sourcePage,
      });
    },

    onSubmit(event) {
      const keyword = event && event.detail && event.detail.value ? event.detail.value : this.data.keyword;
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

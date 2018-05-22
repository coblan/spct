var banner_logic= {
    mounted: function () {
        var self = this
        ex.assign(this.op_funs, {
            online: function () {
                self.set_banner_state(1)
            },
            offline: function () {
                self.set_banner_state(0)
            }
        })
    },

    methods: {
        set_banner_state: function (state) {
            var self = this
            var post_data = [{fun: 'set_banner_status', rows: this.selected, status: state}]
            cfg.show_load()
            ex.post('/d/ajax/' + app, JSON.stringify(post_data), function (resp) {
                cfg.hide_load(2000)
                ex.each(self.selected, function (item) {
                    item.status = state
                })
            })
        },
    }
}

window.banner_logic = banner_logic
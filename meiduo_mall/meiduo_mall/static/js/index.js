const {createApp} = Vue;

const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            username: getCookie('username'),
            f1_tab: 1, // 1F 标签页控制
            f2_tab: 1, // 2F 标签页控制
            f3_tab: 1, // 3F 标签页控制

            // 渲染首页购物车数据
            cart_total_count: 0,
            carts: [],
        }
    },
    methods: {
        // 获取简单购物车数据
        async get_carts() {
            try {
                let url = '/carts/simple/';
                const response = await axios.get(url, {
                    responseType: 'json',
                });

                this.carts = response.data.cart_skus;
                this.cart_total_count = 0;

                for (let i = 0; i < this.carts.length; i++) {
                    if (this.carts[i].name.length > 25) {
                        this.carts[i].name = this.carts[i].name.substring(0, 25) + '...';
                    }
                    this.cart_total_count += this.carts[i].count;
                }
            } catch (error) {
                console.log(error.response);
            }
        }
    },
    // Vue 3 生命周期
    mounted() {
        // 可以在组件挂载后自动获取购物车数据
        this.get_carts();
    }
});

app.mount('#app');
const {createApp} = Vue

const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            username: '',
            password: '',

            error_username: false,
            error_password: false,
            remembered: false,
        }
    },
    methods: {
        // 检查账号
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_username = false;
            } else {
                this.error_username = true;
            }
        },
        // 检查密码
        check_password() {
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 表单提交
        on_submit(event) {
            this.check_username();
            this.check_password();

            if (this.error_username === true || this.error_password === true) {
                // 不满足登录条件：禁用表单
                event.preventDefault();
            }
        },
        // qq登录
        qq_login() {
            let next = getQueryString('next') || '/'
            let url = '/qq/login/?next=' + next
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    location.href = response.data.login_url;

                })
                .catch(error => {
                    console.log(error.response)

                })
        }
    }
})

app.mount('#app')
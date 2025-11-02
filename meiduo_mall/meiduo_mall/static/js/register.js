// Vue3中需要先创建app实例，在配置全局选项
const {createApp} = Vue;

const app = createApp({
    data() {
        return {
            // v-model
            username: '',
            password: '',
            password2: '',
            mobile: '',
            // Vue 3 建议初始化为布尔值（而非空字符串）
            allow: false,
            image_code_url: '',
            uuid: '',
            image_code: '',
            // v-show
            error_name: false,
            error_password: false,
            error_password2: false,
            error_mobile: false,
            error_allow: false,
            // error_message
            error_name_message: '',
            error_mobile_message: '',
            error_image_code_message: '',
            error_image_code: false,

        }
    },
    mounted() { // 页面加载完会被调用mounted函数
        // 生成图形验证码
        this.generate_image_code()
    },
    methods: {
        // 生成图形验证码的方法：封装的思想，实现代码复用，在mounted中可以直接调用
        generate_image_code() {
            this.uuid = generateUUID()
            this.image_code_url = '/image_codes/' + this.uuid + '/'
        },
        // 校验用户名
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_name = false;
            } else {
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            }

            // 判断用户名是否重复
            if (this.error_name === false) {
                // 只有当用户输入的用户名满足条件时才需要判断是否重复
                // 需要先在register.html中导入 axios 模块：
                //     <script type="text/javascript" src="{{ static('js/axios-1.13-min.js') }}"></script>
                //     200 进入 then()  response 是成功的报文
                //     错误进入 catch()  error 是失败的报文.
                let url = '/usernames/' + this.username + '/count/'
                axios.get(url, {responseType: 'json'})
                    .then(response => {
                        if (response.data.count === 1) {
                            this.error_name_message = '用户名已存在'
                            this.error_name = true
                        } else {
                            this.error_name = false
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
        // 校验密码
        check_password() {
            let re = /^[0-9A-Za-z]{8,20}$/;
            this.error_password = !re.test(this.password);

        },
        // 校验确认密码
        check_password2() {
            this.error_password2 = this.password !== this.password2;
        },
        // 校验手机号
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }

            // 判断手机号是否重复
            if (this.error_mobile === false) {
                let url = '/mobiles/' + this.mobile + '/count/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count === 1) {
                            this.error_mobile_message = '手机号已存在';
                            this.error_mobile = true;
                        } else {
                            this.error_mobile = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }

        },
        // 校验是否勾选协议
        check_allow() {
            this.error_allow = !this.allow;
        },
        // 图形验证码校验
        check_image_code() {
            if (this.image_code.length !== 4) {
                this.error_image_code_message = '请填写图片验证码';
                this.error_image_code = true;
            } else {
                this.error_image_code = false;
            }
        },
        // 监听表单提交事件
        on_submit(event) {
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();
            this.check_image_code();
            if (this.error_name === true || this.error_password === true || this.error_password2 === true
                || this.error_mobile === true || this.error_allow === true) {
                // 禁用表单的提交
                event.preventDefault()
            }
        },
    }
})

// 4. 关键：配置模板语法分隔符（Vue 3 中需在 app 实例上设置，而非组件内）
app.config.compilerOptions.delimiters = ['[[', ']]'];

// 5. 挂载 app 实例（替代 Vue 2 的 new Vue().$mount('#app')）
app.mount('#app');

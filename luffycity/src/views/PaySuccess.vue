<template>
    <div class="pay-success">
        <!--如果是单独的页面，就没必要展示导航栏(带有登录的用户)-->
        <!--<Header/>-->
        <div class="main">
            <div class="title">
                <div class="success-tips">
                    <p class="tips">您已成功购买 1 门课程！</p>
                </div>
            </div>
            <div class="order-info">
                <p class="info"><b>订单号：</b><span>{{ result.out_trade_no }}</span></p>
                <p class="info"><b>交易号：</b><span>{{ result.trade_no }}</span></p>
                <p class="info"><b>付款时间：</b><span><span>{{ result.timestamp }}</span></span></p>
            </div>
            <div class="study">
                <span>立即学习</span>
            </div>
        </div>
        <!--<Footer/>-->
    </div>
</template>

<script>
    // import Header from "@/components/Header"
    // import Footer from "@/components/Footer"
    // `
    // ?charset=utf-8&
    // out_trade_no=050195410997&
    // method=alipay.trade.page.pay.return&
    // total_amount=39.00&
    // sign=HSF70z5AkKlu7lzOh%2Bnw8djgFdZe4rS%2BQf6xkPM3cwrVrV0bNl%2Fc8S%2FBarWFzzARlCJ71et37v7WQ%2F7NcP8o2zrJXIio83y7iI9XpNLpjPPm8hLjuG%2FZkMy1Im9aB4CISiGWXK9joo4OnUee6yApRPzw3ZQPBCTj%2Fe1tX8EyZudLCVcWKB6kBl4%2FFmHvPkXbkXznS7jwPpENfCH%2FJ%2B%2BvuTnr1QHyUXygOkkAqVcHfutSq%2Bwa0rvtZyUonymCRpUvQgKjwMzf6ysVIJTwvS6j4ni2rhvtGGkST%2BBtOGulOZNEvzMgbPWt5NMH8N62I3KUzzask0%2BAwofVCNSMyhACcA%3D%3D&
    // trade_no=2020011522001464021000193413&
    // auth_app_id=2016093000631831&version=1.0
    // &app_id=2016093000631831&
    // sign_type=RSA2&
    // seller_id=2088102177958114&
    // timestamp=2020-01-15%2009%3A04%3A50
    // `;
    export default {
        name: "Success",
        data() {
            return {
                result: {},
            };
        },
        created() {
            // url后拼接的参数
            console.log(location.search);

            // url后拼接的参数为空，不用解析
            if (location.search.length === 0) return false;

            // 解析支付宝回调的url参数
            let params = location.search.substring(1);  // 从索引1开始截取到最后
            let items = params.length ? params.split('&') : [];  // ['key1=value1', ..., 'keyn=valuen']
            //逐个将每一项添加到args对象中
            for (let i = 0; i < items.length; i++) {
                let k_v = items[i].split('=');
                //解码操作，因为查询字符串经过编码的
                let k = decodeURIComponent(k_v[0]);
                let v = decodeURIComponent(k_v[1]);
                // let k = k_v[0];
                // let v = k_v[1];
                this.result[k] = v;
            }
            console.log(this.result);



            // 把地址栏上面的支付结果，转发给后端
            this.$axios({
                url: this.$settings.base_url + '/order/pay/success/' + location.search,
                method: 'get'
            }).then(response => {
                console.log(response.data);
            }).catch(() => {
                console.log('支付结果同步失败');
            })
        },
        components: {
            // Header,
            // Footer,
        }
    }
</script>

<style scoped>
    .main {
        padding: 60px 0;
        margin: 0 auto;
        width: 1200px;
        background: #fff;
    }

    .main .title {
        display: flex;
        -ms-flex-align: center;
        align-items: center;
        padding: 25px 40px;
        border-bottom: 1px solid #f2f2f2;
    }

    .main .title .success-tips {
        box-sizing: border-box;
    }

    .title img {
        vertical-align: middle;
        width: 60px;
        height: 60px;
        margin-right: 40px;
    }

    .title .success-tips {
        box-sizing: border-box;
    }

    .title .tips {
        font-size: 26px;
        color: #000;
    }


    .info span {
        color: #ec6730;
    }

    .order-info {
        padding: 25px 48px;
        padding-bottom: 15px;
        border-bottom: 1px solid #f2f2f2;
    }

    .order-info p {
        display: -ms-flexbox;
        display: flex;
        margin-bottom: 10px;
        font-size: 16px;
    }

    .order-info p b {
        font-weight: 400;
        color: #9d9d9d;
        white-space: nowrap;
    }

    .study {
        padding: 25px 40px;
    }

    .study span {
        display: block;
        width: 140px;
        height: 42px;
        text-align: center;
        line-height: 42px;
        cursor: pointer;
        background: #ffc210;
        border-radius: 6px;
        font-size: 16px;
        color: #fff;
    }
</style>
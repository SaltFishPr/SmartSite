import axios from 'axios'

const service = axios.create({
    method: "post",
    baseURL: "http://127.0.0.1:8000/",
    timeout: 10000,
    transformRequest: data => {
        let transData = new URLSearchParams(); //django接收的数据应该为URLSearchParams对象
        transData.append("data", JSON.stringify(data));  //将data对象转换成JSON字符串传输
        return transData;
    }
})

export default service
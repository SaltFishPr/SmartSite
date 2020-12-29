package com.example.smart_site_android;


import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;


public class MainActivity extends AppCompatActivity {
    private EditText etEmployeeId,etEmployeeName;
    private Button btnLogin;
    private ProgressDialog dialog;
    private final ConfigParameter configParameter = new ConfigParameter();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initView();

    }
    private final View.OnClickListener onClickListener = new View.OnClickListener(){

        @Override
        public void onClick(View v) {
            if(v==btnLogin){
                //数据找寻用户名 没有则insert 存在判断密码是否正确 进行跳转
                String employee_id = etEmployeeId.getText().toString();
                String employee_name = etEmployeeName.getText().toString();
                LoginOrRegisterTask loginOrRegisterTask = new LoginOrRegisterTask();
                loginOrRegisterTask.execute(employee_id,employee_name);

            }
        }
    };


    private void initView(){
        etEmployeeId = (EditText)findViewById(R.id.employee_id);
        etEmployeeName = (EditText)findViewById(R.id.employee_name);
        btnLogin = (Button)findViewById(R.id.login);
        btnLogin.setOnClickListener(onClickListener);


        dialog = new ProgressDialog(MainActivity.this);
        dialog.setTitle("温馨提示");
        dialog.setMessage("数据加载中，请耐心等待...");
        dialog.setCancelable(false);//能否在显示过程中关闭
        dialog.setIndeterminate(false);


    }

    private class LoginOrRegisterTask extends AsyncTask<String, Void, Integer>{
        private String response_message;
        private int ret_code; // -2 注册失败 -1 密码错误 0注册成功 1登陆成功 2Json获取失败 3网络请求失败
        private String message;
        private String employee_id;
        String employee_name;
        @Override
        protected Integer doInBackground(String... strings) {
            employee_id = strings[0];
            employee_name = strings[1];
            String url = configParameter.getUrl()+"auth/employee_login";
            Log.d("url",url);
            OkHttpClient client = new OkHttpClient();
            RequestBody requestBody = new FormBody.Builder()
                    .add("employee_id", employee_id)
                    .add("employee_name", employee_name)
                    .build();
            Request request = new Request.Builder()
                    .url(url)
                    .post(requestBody)
                    .build();

            try {
                Response response = client.newCall(request).execute();
                response_message = response.body().string();
            } catch (IOException e) {
                e.printStackTrace();
                return 3; //未能接受网络请求
            }
            try {
                JSONObject jsonObject = new JSONObject(response_message);
                message = jsonObject.get("message").toString();
                ret_code = (int)jsonObject.get("ret_code");
            } catch (JSONException e) {
                e.printStackTrace();
                return 2; //Json数据读取失败
            }

            return ret_code;
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            dialog.show();
        }

        @Override
        protected void onPostExecute(Integer integer) {
            super.onPostExecute(integer);
            switch (integer){
                case 1:
                    dialog.dismiss();
                    Intent intent = new Intent();
                    intent.setClass(MainActivity.this, UploadActivity.class);
                    intent.putExtra("employee_name", employee_name);
                    intent.putExtra("employee_id", employee_id);
                    startActivity(intent);
                    break;
                case 2:
                    dialog.dismiss();
                    Toast.makeText(MainActivity.this,"Json数据读取失败",Toast.LENGTH_SHORT).show();
                    break;
                case 3:
                    dialog.dismiss();
                    Toast.makeText(MainActivity.this,"网络异常，请稍后重试",Toast.LENGTH_SHORT).show();
                    break;
                default:
                    dialog.dismiss();
                    Toast.makeText(MainActivity.this,message,Toast.LENGTH_SHORT).show();

            }

        }
    }
}
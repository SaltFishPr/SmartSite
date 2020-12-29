package com.example.smart_site_android;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.Image;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.text.TextUtils;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class UploadActivity extends AppCompatActivity {
    private String employee_id;
    private String project_id2Send;
    private String check_system_route;
    private String problem_description;
    private File image_file;
    private String riskValue = "-1";


    private static final int PHOTO_GET = 1;
    private static final int PHOTO_RESOULT = 2;// 结果
    private long exitTime = 0;

    private String employee_name;
    private TextView tvUserId,tvFirstCheckId;
    private final ConfigParameter configParameter = new ConfigParameter();
    private Spinner spGroupName = null;
    private Spinner spProjectName = null;
    private Spinner spOneRoute = null;
    private Spinner spTwoRoute = null;
    private Spinner spThreeRoute = null;
    private ImageView imageView = null;
    private Button btnSelectImage = null;
    private EditText etProblemDescription = null;
    private Button btnSubmit = null;
    private ProgressDialog dialog;
    private RadioGroup radioGroup = null;
    private RadioButton rbSafe,rbLowRisk,rbDangerous = null;

    private ArrayList<String> projects = new ArrayList<>();//存放项目名称
    private ArrayList<String> projects_id = new ArrayList<>();//存放项目id
    private ArrayList<String> groups = new ArrayList<>(); //用户所在小组列表
    private ByteArrayOutputStream stream = new ByteArrayOutputStream();//上传的图片流
    private ArrayList<String> firstCheckSystemId = new ArrayList<>();; //第一级检查体系ID
    private String firstCheckSystem; //第一级检查体系描述
    private int firstCheckIndex; // 定位第一级检查列表的位置
    private ArrayList<String> secondRoute = new ArrayList<>(); //存放第二级检查体系描述
    private ArrayList<String> secondRouteId = new ArrayList<>(); //存放第二级检查体系ID
    private String node1,node2;





    private SpinnerAdapter spinnerAdapter = null;
    private SpinnerAdapter spinnerProjectAdapter = null;
//    private SpinnerAdapter spinnerFirstRouteAdapter = null;
    private SpinnerAdapter spinnerSecondRoutAdapter = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_upload);
        initData();
        getCheckInfoFromServer();
        initView();
        getEmployeeInfoFromServer();


    }


    private final View.OnClickListener onClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if(v==btnSelectImage){
                //选择图片
                Intent intent = new Intent(Intent.ACTION_PICK, null);
                intent.setDataAndType(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, "image/*");
                startActivityForResult(intent,PHOTO_GET);
            }else if (v==btnSubmit){
                //提交按钮
                if (project_id2Send == null){
                    Toast.makeText(UploadActivity.this,"请选择项目后再进行提交",Toast.LENGTH_SHORT).show();
                }
                else{
                    if (TextUtils.isEmpty(etProblemDescription.getText())){
                        Toast.makeText(UploadActivity.this,"请填写问题描述后再进行提交",Toast.LENGTH_SHORT).show();
                    }else{
                        if(imageView.getDrawable() == null)
                        {
                            Toast.makeText(UploadActivity.this,"请选择图片后再进行提交",Toast.LENGTH_SHORT).show();
                        }else{
                            if(riskValue == "-1"){
                                Toast.makeText(UploadActivity.this,"请选择风险等级后再进行提交",Toast.LENGTH_SHORT).show();
                            }else{
                                problem_description = etProblemDescription.getText().toString();
                                check_system_route = node1+"-"+node2;
                                SendTask sendTask = new SendTask();
                                sendTask.execute(image_file);
                            }


//                            new Thread(new Runnable(){
//                                @Override
//                                public void run() {
//                                    SendTask sendTask = new SendTask();
//                                    try {
//                                        String message = null;
//                                        message = sendTask.sendFromDataPostRequest(image_file);
//                                        Toast.makeText(UploadActivity.this,message,Toast.LENGTH_SHORT).show();
//                                    } catch (IOException e) {
//                                        e.printStackTrace();
//                                    }
//                                }
//                            }).start();
                        }

                    }

                }

            }
        }
    };


    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if( keyCode== KeyEvent.KEYCODE_HOME){
            return true;
        } else if( keyCode== KeyEvent.KEYCODE_BACK && event.getAction() == KeyEvent.ACTION_DOWN){
            if((System.currentTimeMillis()- exitTime) > 2000){
                Toast.makeText(getApplicationContext(), "再按一次退出账户", Toast.LENGTH_SHORT).show();
                exitTime = System.currentTimeMillis();
            } else {
                finish();
                System.exit(0);
            }
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    private void initView(){
        tvFirstCheckId = (TextView)findViewById(R.id.firstRouteCheck);
        tvUserId = (TextView)findViewById(R.id.tvUserId);
        tvUserId.setText("用户名:"+employee_name);
        spGroupName = (Spinner)findViewById(R.id.spinnerGroupName);
        spProjectName = (Spinner) findViewById(R.id.spinnerProjectName);
//        spOneRoute = (Spinner) findViewById(R.id.spinnerRouteOne);
        spTwoRoute = (Spinner) findViewById(R.id.spinnerRouteTwo);
        imageView = (ImageView) findViewById(R.id.imageView);
        etProblemDescription = (EditText)findViewById(R.id.et_description);
        btnSubmit = (Button) findViewById(R.id.btn_submit);
        btnSubmit.setOnClickListener(onClickListener);
        btnSelectImage = (Button)findViewById(R.id.btn_select);
        btnSelectImage.setOnClickListener(onClickListener);
        radioGroup = (RadioGroup)findViewById(R.id.radio_group);
        rbDangerous = (RadioButton)findViewById(R.id.dangerous);
        rbLowRisk = (RadioButton)findViewById(R.id.low_risk);
        rbSafe = (RadioButton)findViewById(R.id.safe);
        radioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                switch (checkedId){
                    case R.id.safe:
                        riskValue = "0";
                        break;
                    case R.id.low_risk:
                        riskValue = "1";
                        break;
                    case R.id.dangerous:
                        riskValue = "4";
                        break;
                    default:
                        riskValue = "-1";
                        break;
                }
            }
        });


        dialog = new ProgressDialog(UploadActivity.this);
        dialog.setTitle("温馨提示");
        dialog.setMessage("数据发送中，请耐心等待...");
        dialog.setCancelable(false);//能否在显示过程中关闭
        dialog.setIndeterminate(false);
    }


    private void initData(){
        Intent intent =getIntent();
        employee_name = intent.getStringExtra("employee_name");
        employee_id = intent.getStringExtra("employee_id");

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == 0)
            return;
        if (data == null)
            return;
        // 读取相册缩放图片
        if (requestCode == PHOTO_GET) {
            stream.reset();
            startPhotoZoom(data.getData());
        }
        if (requestCode == PHOTO_RESOULT){
            Bundle extras = data.getExtras();
            if (extras != null) {
                Bitmap photo = extras.getParcelable("data");
                photo.compress(Bitmap.CompressFormat.JPEG, 75, stream);// (JPEG格式，压缩率（0-100）,写入压缩数据的输出流) 如果成功地把压缩数据写入输出流，则返回true。
                image_file= convertBitmapToFile();
                //把图片显示在ImageView控件上
                imageView.setImageBitmap(photo);
            }
        }


    }

    private void bindView(){
        spinnerAdapter = new SpinnerAdapter(groups,UploadActivity.this);
        spGroupName.setAdapter(spinnerAdapter);
        spGroupName.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                //点击相应项目之后，相关信息刷新
                //Toast.makeText(UploadActivity.this,"你选择了:"+spinnerAdapter.getItem(position),Toast.LENGTH_SHORT).show();

                projects.clear();
                projects_id.clear();
                project_id2Send = null;
                firstCheckSystemId.clear();
                firstCheckSystem = null;
                secondRoute.clear();
                secondRouteId.clear();
                tvFirstCheckId.setText("第一级检查体系(选择项目后获取)");
                bindRouteView(2);
                GetProjectInfoTask getProjectInfoTask = new GetProjectInfoTask();
                getProjectInfoTask.execute(spinnerAdapter.getItem(position).toString());

            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                Toast.makeText(UploadActivity.this, "请重新选择",
                        Toast.LENGTH_SHORT).show();
            }
        });

    }

    private void bindProjectView(){
        spinnerProjectAdapter = new SpinnerAdapter(projects,UploadActivity.this);
        spProjectName.setAdapter(spinnerProjectAdapter);
        spProjectName.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                if (projects.size() == 0){
                    Toast.makeText(UploadActivity.this, "该小组没有执行项目,请重新选择",
                            Toast.LENGTH_SHORT).show();
                    tvFirstCheckId.setText("第一级检查体系(选择项目后获取)");
                    secondRoute.clear();
                    secondRouteId.clear();
                    bindRouteView(2);
                }else{
                    //Toast.makeText(UploadActivity.this,"你选择了:"+ projects_id.get(position),Toast.LENGTH_SHORT).show();
                    project_id2Send = projects_id.get(position).toString();
                    firstCheckIndex = position;
                    secondRoute.clear();
                    secondRouteId.clear();
                    GetFirstCheckSystemTask getFirstCheckSystemTask = new GetFirstCheckSystemTask();
                    getFirstCheckSystemTask.execute(firstCheckSystemId.get(position).toString());
                }

            }
            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                Toast.makeText(UploadActivity.this, "请重新选择",
                        Toast.LENGTH_SHORT).show();
            }
        });
    }


    private void bindRouteView(int level){
        if (level == 1){
            //第一级检查体系取消下拉，变成TextView
            secondRoute.clear();
            secondRouteId.clear();
            tvFirstCheckId.setText("第一级检查体系:"+firstCheckSystem);
            GetRouteTwoTask getRouteTwoTask = new GetRouteTwoTask();
            getRouteTwoTask.execute(firstCheckSystemId.get(firstCheckIndex));
//            spinnerFirstRouteAdapter = new SpinnerAdapter(firstRoute,UploadActivity.this);
//            spOneRoute.setAdapter(spinnerFirstRouteAdapter);
//            spOneRoute.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
//                @Override
//                public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
//                    node1 = firstRouteId.get(position).toString();
//                    node2 = null;
//                    secondRoute.clear();
//                    secondRouteId.clear();
//                    GetRouteTwoTask getRouteTwoTask = new GetRouteTwoTask();
//                    getRouteTwoTask.execute(firstRouteId.get(position).toString());
//                }
//                @Override
//                public void onNothingSelected(AdapterView<?> parent) {
//                    Toast.makeText(UploadActivity.this, "请重新选择",
//                            Toast.LENGTH_SHORT).show();
//                }
//            });
        }else if (level ==2){ //第二级检查体系
            spinnerSecondRoutAdapter = new SpinnerAdapter(secondRoute,UploadActivity.this);
            spTwoRoute.setAdapter(spinnerSecondRoutAdapter);
            spTwoRoute.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                @Override
                public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                    node2 = secondRouteId.get(position).toString();
//                    GetRouteThreeTask getRouteThreeTask = new GetRouteThreeTask();
//                    getRouteThreeTask.execute(secondRouteId.get(position));
                }
                @Override
                public void onNothingSelected(AdapterView<?> parent) {
                    Toast.makeText(UploadActivity.this, "请重新选择",
                            Toast.LENGTH_SHORT).show();
                }
            });
        }else if (level ==3){
            //取消第三级检查
        }

    }







    private void startPhotoZoom(Uri uri){
        Intent intent = new Intent("com.android.camera.action.CROP");//调用Android系统自带的一个图片剪裁页面,
        intent.setDataAndType(uri, "image/*");
        intent.putExtra("crop", "true");//进行修剪
        // aspectX aspectY 是宽高的比例
        intent.putExtra("aspectX", 1);
        intent.putExtra("aspectY", 1);
        // outputX outputY 是裁剪图片宽高
        intent.putExtra("outputX", 500);
        intent.putExtra("outputY", 500);
        intent.putExtra("return-data", true);
        startActivityForResult(intent, PHOTO_RESOULT);
    }


    private File convertBitmapToFile() {
        Bitmap phonto = BitmapFactory.decodeByteArray(stream.toByteArray(), 0, stream.toByteArray().length);
        ByteArrayOutputStream compressBuffer = new ByteArrayOutputStream();
        phonto.compress(Bitmap.CompressFormat.JPEG, 100,compressBuffer);//质量压缩方法，这里100表示不压缩，把压缩后的数据存放到compressBuffer中
        int options = 100;
        while (compressBuffer.toByteArray().length / 1024 > 20) {  //循环判断如果压缩后图片是否大于20kb,大于继续压缩
            compressBuffer.reset();//重置Buffer
            options -= 10;//每次都减少10
            phonto.compress(Bitmap.CompressFormat.JPEG, options, compressBuffer);//这里压缩options%，把压缩后的数据存放到compressBuffer中
            long length = compressBuffer.toByteArray().length;
        }
        SimpleDateFormat format = new SimpleDateFormat("yyyyMMddHHmmss");
        Date date = new Date(System.currentTimeMillis());
        String filename = format.format(date);
        File file = new File(Environment.getExternalStorageDirectory(), filename + ".png");
        try {
            FileOutputStream fos = new FileOutputStream(file);
            try {
                fos.write(compressBuffer.toByteArray());
                fos.flush();
                fos.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        return file;
    }

    private void getEmployeeInfoFromServer(){
//        GetRouteOneTask getRouteOneTask = new GetRouteOneTask();
//        getRouteOneTask.execute();
    }
    private void getCheckInfoFromServer(){
        GetEmployeeInfoTask getEmployeeInfoTask = new GetEmployeeInfoTask();
        getEmployeeInfoTask.execute();
    }

    private class GetProjectInfoTask extends AsyncTask<String, Void, Integer>{
        private String response_message;
        private JSONArray descriptionArray,idArray,checkArray;
        @Override
        protected Integer doInBackground(String... strings) {
            String group_id = strings[0];
            JSONObject jsonObject2Send = new JSONObject();
            try {
                jsonObject2Send.put("group_id",group_id);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            String url = configParameter.getUrl() + "project/get_by_group";
            OkHttpClient client = new OkHttpClient();
            RequestBody requestBody = new FormBody.Builder()
                    .add("data", String.valueOf(jsonObject2Send))
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
                descriptionArray = jsonObject.getJSONArray("project_list");
                idArray = jsonObject.getJSONArray("id_list");
                checkArray = jsonObject.getJSONArray("check_id_list");
                for (int i =0; i<descriptionArray.length();i++){
                    projects.add(descriptionArray.get(i).toString());
                    projects_id.add(idArray.get(i).toString());
                    firstCheckSystemId.add(checkArray.get(i).toString());
                }

            } catch (JSONException e) {
                e.printStackTrace();

                return 2; //Json数据读取失败
            }

            return 1;
        }

        @Override
        protected void onPostExecute(Integer integer) {
            super.onPostExecute(integer);
            switch (integer){
                case 1:
                    Log.d("projects信息:",projects.toString());
                    bindProjectView();
                    break;
//                case 2:
//                    Toast.makeText(UploadActivity.this,"Json数据读取失败",Toast.LENGTH_SHORT).show();
//                    break;
//                case 3:
//                    Toast.makeText(UploadActivity.this,"网络异常，请稍后重试",Toast.LENGTH_SHORT).show();
//                    break;
//                default:
//                    Toast.makeText(UploadActivity.this,"系统异常",Toast.LENGTH_SHORT).show();
            }
        }
    }

    private class GetEmployeeInfoTask extends AsyncTask<String, Void, Integer>{
        private String response_message;
        private JSONArray jsonArray;
        @Override
        protected Integer doInBackground(String... strings) {
            JSONObject jsonObject2Send = new JSONObject();
            try {
                jsonObject2Send.put("employee_id",employee_id);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            String url = configParameter.getUrl() + "employee/get_groups";
            OkHttpClient client = new OkHttpClient();
            RequestBody requestBody = new FormBody.Builder()
                    .add("data", String.valueOf(jsonObject2Send))
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
                jsonArray = (JSONArray) jsonObject.get("group_list");

                for (int i =0; i<jsonArray.length();i++){
                    groups.add(jsonArray.get(i).toString());
                }

            } catch (JSONException e) {
                e.printStackTrace();
                return 2; //Json数据读取失败
            }

            return 1;
        }

        @Override
        protected void onPostExecute(Integer integer) {
            super.onPostExecute(integer);
            switch (integer){
                case 1:
                    bindView();
                    break;
                case 2:
                    Toast.makeText(UploadActivity.this,"Json数据读取失败",Toast.LENGTH_SHORT).show();
                    break;
                case 3:
                    Toast.makeText(UploadActivity.this,"网络异常，请稍后重试",Toast.LENGTH_SHORT).show();
                    break;
                default:
                    Toast.makeText(UploadActivity.this,"系统异常",Toast.LENGTH_SHORT).show();
            }
        }
    }

//    private class GetRouteOneTask extends  AsyncTask<String, Void, Integer>{
//        private String response_message;
//        private JSONArray jsonArray,idArray;
//        @Override
//        protected Integer doInBackground(String... strings) {
//            String url = configParameter.getUrl() + "system/get_first_route";
//            OkHttpClient client = new OkHttpClient();
//            RequestBody requestBody = new FormBody.Builder()
//                    .build();
//
//            Request request = new Request.Builder()
//                    .url(url)
//                    .post(requestBody)
//                    .build();
//
//            try {
//                Response response = client.newCall(request).execute();
//                response_message = response.body().string();
//
//            } catch (IOException e) {
//                e.printStackTrace();
//                return 3; //未能接受网络请求
//            }
//            try {
//                JSONObject jsonObject = new JSONObject(response_message);
//                jsonArray = (JSONArray) jsonObject.get("first_system");
//                idArray = (JSONArray)jsonObject.getJSONArray("id_list");
//                for (int i =0; i<jsonArray.length();i++){
//                    firstRoute.add(jsonArray.get(i).toString());
//                    firstRouteId.add(idArray.get(i).toString());
//
//                }
//
//            } catch (JSONException e) {
//                e.printStackTrace();
//                return 2; //Json数据读取失败
//            }
//
//            return 1;
//        }
//
//        @Override
//        protected void onPostExecute(Integer integer) {
//            super.onPostExecute(integer);
//            switch (integer){
//                case 1:
//                    bindRouteView(1);
//                    break;
//                case 2:
//                    Toast.makeText(UploadActivity.this,"Json数据读取失败",Toast.LENGTH_SHORT).show();
//                    break;
//                case 3:
//                    Toast.makeText(UploadActivity.this,"网络异常，请稍后重试",Toast.LENGTH_SHORT).show();
//                    break;
//                default:
//                    Toast.makeText(UploadActivity.this,"系统异常",Toast.LENGTH_SHORT).show();
//            }
//        }
//    }

    private class GetRouteTwoTask extends AsyncTask<String, Void, Integer>{
        private String response_message;
        private JSONArray descriptionArray,idArray;
        @Override
        protected Integer doInBackground(String... strings) {
            String first_id = strings[0];
            node1 = first_id;
            JSONObject jsonObject2Send = new JSONObject();
            try {
                jsonObject2Send.put("first_id",first_id);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            String url = configParameter.getUrl() + "system/get_second_route";
            OkHttpClient client = new OkHttpClient();
            RequestBody requestBody = new FormBody.Builder()
                    .add("data", String.valueOf(jsonObject2Send))
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
                descriptionArray = jsonObject.getJSONArray("sencond_system");
                idArray = jsonObject.getJSONArray("id_list");
                for (int i =0; i<descriptionArray.length();i++){
                    secondRoute.add(descriptionArray.get(i).toString());
                    secondRouteId.add(idArray.get(i).toString());
                }
                Log.d("routeId",secondRouteId.toString());
                Log.d("routeDescription",secondRoute.toString());

            } catch (JSONException e) {
                e.printStackTrace();

                return 2; //Json数据读取失败
            }

            return 1;
        }

        @Override
        protected void onPostExecute(Integer integer) {
            super.onPostExecute(integer);
            switch (integer){
                case 1:
                    bindRouteView(2);
                    break;
                case 2:
                    Toast.makeText(UploadActivity.this,"Json数据读取失败",Toast.LENGTH_SHORT).show();
                    break;
                case 3:
                    Toast.makeText(UploadActivity.this,"网络异常，请稍后重试",Toast.LENGTH_SHORT).show();
                    break;
                default:
                    Toast.makeText(UploadActivity.this,"系统异常",Toast.LENGTH_SHORT).show();
            }
        }
    }




    private class GetFirstCheckSystemTask extends AsyncTask<String, Void, Integer>{
        private String response_message,checkSystem;
        @Override
        protected Integer doInBackground(String... strings) {
            String check_info_id = strings[0];
            JSONObject jsonObject2Send = new JSONObject();
            try {
                jsonObject2Send.put("check_info_id",check_info_id);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            String url = configParameter.getUrl() + "system/get_check_info";
            OkHttpClient client = new OkHttpClient();
            RequestBody requestBody = new FormBody.Builder()
                    .add("data", String.valueOf(jsonObject2Send))
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
                firstCheckSystem = jsonObject.getString("first_system");
            } catch (JSONException e) {
                e.printStackTrace();

                return 2; //Json数据读取失败
            }

            return 1;
        }

        @Override
        protected void onPostExecute(Integer integer) {
            super.onPostExecute(integer);
            switch (integer){
                case 1:
                    bindRouteView(1);
                    break;
                case 2:
                    Toast.makeText(UploadActivity.this,"Json数据读取失败",Toast.LENGTH_SHORT).show();
                    break;
                case 3:
                    Toast.makeText(UploadActivity.this,"网络异常，请稍后重试",Toast.LENGTH_SHORT).show();
                    break;
                default:
                    Toast.makeText(UploadActivity.this,"系统异常",Toast.LENGTH_SHORT).show();
            }
        }
    }




    private class SendTask extends AsyncTask<File,Void,String> {
        private String response_message;
        private String message = "未打开服务器";
        public  String sendFromDataPostRequest(File file)throws IOException{
            RequestBody fileBody = RequestBody.create(MediaType.parse("image/png"),file);
            OkHttpClient client = new OkHttpClient();
            RequestBody requestBody = new MultipartBody.Builder()
                    .setType(MultipartBody.FORM)
                    .addFormDataPart("Image","check.png",fileBody)
                    .addFormDataPart("project_id", project_id2Send)
                    .addFormDataPart("check_system_route", check_system_route)
                    .addFormDataPart("employee_id", employee_id)
                    .addFormDataPart("problem_description", problem_description)
                    .addFormDataPart("risk_value",riskValue)
                    .build();
            Request request = new Request.Builder()
                    .post(requestBody)
                    .url(configParameter.getUrl()+"check/get_check_info")
                    .build();

            try {
                Response response = client.newCall(request).execute();
                response_message = response.body().string();
            } catch (IOException e) {
                e.printStackTrace();
                JSONObject jsonObject = null;
                try {
                    jsonObject = new JSONObject(response_message);
                    message = jsonObject.get("message").toString();
                } catch (JSONException jsonException) {
                    jsonException.printStackTrace();
                }

            }
            return message;
        }

        @Override
        protected String doInBackground(File... strings) {
            File file = strings[0];
            RequestBody fileBody = RequestBody.create(MediaType.parse("image/png"),file);
            OkHttpClient client = new OkHttpClient();
            RequestBody requestBody = new MultipartBody.Builder()
                    .setType(MultipartBody.FORM)
                    .addFormDataPart("Image","check.png",fileBody)
                    .addFormDataPart("project_id", project_id2Send)
                    .addFormDataPart("check_system_route", check_system_route)
                    .addFormDataPart("employee_id", employee_id)
                    .addFormDataPart("problem_description", problem_description)
                    .addFormDataPart("risk_value",riskValue)
                    .build();
            Request request = new Request.Builder()
                    .post(requestBody)
                    .url(configParameter.getUrl()+"check/get_check_info")
                    .build();

            try {
                Response response = client.newCall(request).execute();
                response_message = response.body().string();
            } catch (IOException e) {
                e.printStackTrace();
                return "网络异常，请稍后再试";
            }
            JSONObject jsonObject = null;
            try {
                jsonObject = new JSONObject(response_message);
                message = jsonObject.get("message").toString();
            } catch (JSONException jsonException) {
                jsonException.printStackTrace();
                return "Json读取失败";
            }
            return message;
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            dialog.show();
        }

        @Override
        protected void onPostExecute(String s) {
            super.onPostExecute(s);
            if (s.equals(null)){
                dialog.dismiss();
                Toast.makeText(UploadActivity.this,"系统异常",Toast.LENGTH_SHORT).show();
            }
            dialog.dismiss();
            Toast.makeText(UploadActivity.this,s,Toast.LENGTH_SHORT).show();
        }
    }

}
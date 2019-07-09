using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.IO;
using System;

public class stickman : MonoBehaviour
{
    private string jsonFile;
    private StreamReader file;
    private JsonTextReader reader;
    private JObject jObject;
    private Animation animation;
    private long timeStamp;
    private long oldTimeStamp = 0;
    private float targetX = 0;
    private float targetZ = 0;
   
    static private readonly string path = "C://Users//zkx74//Desktop//totalTest//database//陈泊舟//interaction//withUnity//control.json";
    private FileInfo fi = new FileInfo(path);
    private string lastAction = "";
    // 这里是类变量 -------------------
    // 记录转身前的角度
    private Quaternion raw_rotation;
    // 准备面向的角度
    private Quaternion lookat_rotation;
    // 转身速度(每秒能转多少度)  
    private float per_second_rotate = 1080.0f;
    // 旋转角度越大, lerp变化速度就应该越慢 
    float lerp_speed = 0.0f;
    // lerp的动态参数
    float lerp_tm = 0.0f;
    // --------------------------------


    // 旋转之前的初始化
    void Init_Rotate(Vector3 move_location_pos)
    {
        // 记录转身前的角度
        raw_rotation = transform.rotation;
        // 记录目标角度
        transform.LookAt(move_location_pos);
        lookat_rotation = transform.rotation;
        // 还原当前角度
        transform .rotation = raw_rotation;
        // 计算旋转角度
        float rotate_angle = Quaternion.Angle(raw_rotation, lookat_rotation);
        // 获得lerp速度
        lerp_speed = per_second_rotate / rotate_angle;
        Debug.Log("Angle:" + rotate_angle.ToString() + " speed:" + lerp_speed.ToString());
        lerp_tm = 0.0f;
    }
    void jsonReaderInit()
    {
       
        file = File.OpenText(path);
        reader = new JsonTextReader(file);
        jObject = (JObject)JToken.ReadFrom(reader);
        file.Close();
    }
    public string ReadJson(string key)
    {
        if (jObject[key] != null)
        {
            var value = jObject[key].ToString();
            return value;
        }
        else
        {
            return "";
        }
    }
    public string ReadJsonWihtInit(string key)
    {
        jsonReaderInit();
        return ReadJson(key);
    }
    // Start is called before the first frame update
    void Start()
    {
        animation = this.transform.GetComponent<Animation>();
        animation.Stop();
        animation.Rewind();
        jsonReaderInit();
    }
    void updateFile()
    {
        /*if (File.Exists(path))
        {
            File.Delete(path);
        }
        */
        FileStream fs = new FileStream(path, FileMode.Create,FileAccess.Write,FileShare.ReadWrite);
        byte[] empty = System.Text.Encoding.UTF8.GetBytes("{}");
        fs.Write(empty, 0, empty.Length);
        fs.Flush();
        fs.Close();
    }
    long ToTimeStamp(DateTime date)
    {
        DateTime startTime = TimeZone.CurrentTimeZone.ToLocalTime(new DateTime(1970, 1, 1)); // 当地时区
        return (long)(DateTime.Now - date).TotalMilliseconds; // 相差毫秒数
        
    }
    // Update is called once per frame
    void Update()
    {
        string action="";
        float dx=0.0f;
        float dy=0.0f;
        //timeStamp = long.Parse(ReadJsonWihtInit("Time"));
        timeStamp = ToTimeStamp(fi.LastWriteTime);
        //解析指令，执行单帧指令
        if (timeStamp!=oldTimeStamp)
        {
            oldTimeStamp = timeStamp;
            action = ReadJsonWihtInit("operation");
            dx = 0;
            dy = 0;
            if (action.Contains("move"))    
            {
                dx = float.Parse(ReadJsonWihtInit("dx"));
                dy = float.Parse(ReadJsonWihtInit("dy"));
            }
            else if (action.Contains("turn"))
            {
                //指令格式 turn 参数 (参数>0表示顺时针旋转)
                float rotateSpeed = 0.5f;
                string[] temp = action.Split(' ');
                float angles = float.Parse(temp[1]);
                Quaternion targetAngles = Quaternion.Euler(0, transform.rotation.eulerAngles.y + angles, 0);
                // transform.Rotate(new Vector3(0, Time.deltaTime * rotateSpeed, 0));
                transform.rotation = Quaternion.Slerp(transform.rotation, targetAngles, rotateSpeed * Time.deltaTime);
                if (Quaternion.Angle(targetAngles, transform.rotation) < 1)
                {
                    transform.rotation = targetAngles;
                }
            }
            else if (action.Contains("observe"))
            {
                
            }
            else if(lastAction.Equals(""))
            {
                animation.Rewind();
                //animation.Stop();
            }
            updateFile();
        }
        //多帧指令在此执行
        if (action.Contains("move")||lastAction.Contains("move"))
        {
            float moveSpeed = 0.5f;
            float translation = moveSpeed * Time.deltaTime;
            if (!lastAction.Equals("move"))
            {
                targetX = transform.position.x + dx;
                targetZ = transform.position.z + dy;
            }
            //如果未达到指定位置
            if (transform.position.x != targetX || transform.position.z != targetZ)
            {
                //开始播放走路动画
                animation.Play();
                //transform.Translate(Vector3.forward * translation);
                //保持朝向
                transform.LookAt(new Vector3(targetX, transform.position.y, targetZ));
                //移动位置
                transform.localPosition = Vector3.MoveTowards(transform.localPosition, new Vector3(targetX, transform.position.y, targetZ), translation);
                lastAction = "move";
            }
            //已经达到指定位置
            else
            {
                animation.Rewind();
                updateFile();
                lastAction = "";
            }
        }

    }
}

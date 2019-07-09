using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.IO;
using System;

public class Cube : MonoBehaviour
{
    protected float jump_speed = 12.0f;
    protected bool is_landing=false;
    string jsonFile;
    StreamReader file;
    JsonTextReader reader;
    JObject jObject;
    int i = 0;
    void jsonReaderInit(){
        jsonFile="C://Users//zkx74//IdeaProjects//QLearingEnvironment//out//production//resources//action.json";
        file=File.OpenText(jsonFile);
        reader=new JsonTextReader(file);
        jObject=(JObject)JToken.ReadFrom(reader);
    }
    public string ReadJson(string key){
        var value=jObject[key].ToString();
        return value;
    }
    public string ReadJsonWihtInit(string key){
        jsonReaderInit();
        file.Close();
        return ReadJson(key);
    }
    // Start is called before the first frame update
    void Start()
    {
        this.is_landing=false;
        jsonReaderInit();
    }

    // Update is called once per frame
    void Update()
    {
        string action=ReadJsonWihtInit("actionZkx");
        if(this.is_landing)
        {
            if(Input.GetMouseButtonDown(0)||action.Equals("1"))
            {
                this.is_landing=false;
                this.GetComponent<Rigidbody>().velocity=Vector3.up*this.jump_speed;
            }
        }
        i++;
        string s = i.ToString();
        /*
        FileStream fs = new FileStream("C:\\Users\\zkx74\\Desktop\\test.txt", FileMode.Create, FileAccess.ReadWrite, FileShare.ReadWrite);
        byte[] b= System.Text.Encoding.UTF8.GetBytes("Hello World!"+s);
        fs.Write(b, 0, b.Length);
        fs.Flush();
        fs.Close();
        */
        FileStream fs = new FileStream("C:\\Users\\zkx74\\Desktop\\test.txt", FileMode.Open, FileAccess.ReadWrite, FileShare.ReadWrite);
        int len = (int)fs.Length;
        byte[] b = new byte[len];
        int r = fs.Read(b, 0, b.Length);
        string str= System.Text.Encoding.UTF8.GetString(b);
        fs.Close();
        if (str.Length!=0)
        {
            Debug.Log(str);
        }

    }

    void OnCollisionEnter(Collision collisionInfo)
    {
        //Debug.Break();
        if(collisionInfo.gameObject.tag=="Floor"|| collisionInfo.gameObject.tag == "Terrain")
        {
            this.is_landing=true;
        }
    }
}

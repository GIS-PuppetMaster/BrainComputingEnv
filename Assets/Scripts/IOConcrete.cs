using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.IO;
using System;

public class IOConcrete : MonoBehaviour,IOInterface
{
    /// <summary>
    /// 上次读到的命令行数
    /// </summary>
    private long _lastIndex = 0;
    /// <summary>
    /// 保存读入的控制命令
    /// </summary>
    private string _agentControlText;
    /// <summary>
    /// 控制命令读入路径
    /// </summary>
    public string agentControlPath ;
    /// <summary>
    /// 环境信息输出路径
    /// </summary>
    public string envMessagePath ;


    //上一次读取命令时文件的时间戳
    private DateTime _timeStamp;
    //命令文件
    private string _jsonFile;
    //文件读入
    private StreamReader _file;
    private JsonTextReader _reader;
    //当前读取的文件信息
    private FileInfo _fileInfo;
    //读取到的命令
    private JObject _jObject;
    


    /// <summary>
    /// 初始化Json读取
    /// 会读取文件信息和内容，并清空文件
    /// </summary>
    private void JsonReaderInit()
    {
        _file = File.OpenText(agentControlPath);
        _fileInfo = new FileInfo(agentControlPath);
        _reader = new JsonTextReader(_file);
        _reader.SupportMultipleContent = true;
        _jObject = (JObject)JToken.ReadFrom(_reader);
        _file.Close();
        //清空文件
        File.WriteAllText(agentControlPath,"");
        //记录清空文件后的时间戳
        _timeStamp = _fileInfo.LastWriteTime;
    }
    

    /// <summary>
    /// 解析Json，只有时间戳改变时才会解析
    /// 只要调用这个函数，文件内容就会被读取、清空
    /// </summary>
    /// <param name="index">目标key，通常为命令编号</param>
    /// <returns>返回读取到的命令的JObject，如果未找到制定编号的命令则返回null</returns>
    private JObject ParseJsonReturnJObject(long index)
    {
        if (_jObject[index.ToString()] != null)
            {
                var value = _jObject[index.ToString()];
                return (JObject)value;
            }
        return null;
    }

    
    
    public JObject GetAgentControlOrderFromIndex(long index)
    {
        _fileInfo = new FileInfo(agentControlPath);
        if (!_fileInfo.LastWriteTime.Equals(_timeStamp))
        {
            JsonReaderInit();
            _jObject = ParseJsonReturnJObject(index);
            return _jObject;
        }

        return null;
    }

    
    public void OutputEnvMessage(string message)
    {
        File.WriteAllText(envMessagePath,message);
    }

    public List<JObject> GetAgentControlOrder()
    {
        _fileInfo = new FileInfo(agentControlPath);
        if (!_fileInfo.LastWriteTime.Equals(_timeStamp))
        {
            JsonReaderInit();
            List<JObject> list = new List<JObject>();
            for (int i = 1;; i++)
            {
                JObject jObject = ParseJsonReturnJObject(i);
                if (jObject != null)
                {
                    list.Add(jObject);
                }
                else
                {
                    break;
                }
            }
            return list;
        }
        return null;
    }
}

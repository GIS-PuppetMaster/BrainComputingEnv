using System;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;
using UnityEngine;

public class MessageManager
{
    //当前环境中存在的消息集合
    //TODO:保存消息的发送位置
    private readonly ISet<JObject> _messageSet=new HashSet<JObject>();
    /// <summary>
    /// 获取环境中某个agent自己发出的消息
    /// </summary>
    /// <param name="agent">发出消息的agent</param>
    /// <returns>消息</returns>
    public JObject GerMessageAsSender(GameObject agent)
    {
        //TODO
        throw new NotImplementedException();
    }
    
    /// <summary>
    /// 获取环境中发送给自己的消息
    /// 当消息发出者在一定距离内时才能收到消息
    /// </summary>
    /// <param name="agent">接收消息的agent</param>
    /// <returns>消息内容</returns>
    public JObject GetMessageAsReceiver(GameObject agent)
    {
        //TODO
        throw new NotImplementedException();

    }

    
}
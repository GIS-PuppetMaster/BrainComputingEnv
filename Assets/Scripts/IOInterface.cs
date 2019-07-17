using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public interface IOInterface
{
    /// <summary>
    /// 根据命令的编号（第几条）获取对应的命令
    /// </summary>
    /// <param name="index">命令名称</param>
    /// <returns>命令内容JObject</returns>
    JObject GetAgentControlOrderFromIndex(long index);

    /// <summary>
    /// 获取全部命令
    /// </summary>
    /// <returns>命令list</returns>
    List<JObject> GetAgentControlOrder();

    /// <summary>
    /// 输出环境交互信息
    /// </summary>
    /// <param name="message">要输出的环境交互信息</param>
    void OutputEnvMessage(string message);
    
    
        
     
}

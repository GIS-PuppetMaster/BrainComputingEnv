using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using UnityEngine;
using UnityEngine.Animations;

/// <summary>
/// 负责环境事件的监听
///     环境事件包括Agent之间的信息交互
///     Agent对环境信息的感官获取
///     Agent对环境的改变的实现
/// </summary>
public class EnvEventManager
{
    /// <summary>
    /// 环境中存在的消息
    /// </summary>
    public MessageManager _messageManager=new MessageManager();

    public JObject GetMessageAsSender(GameObject agent)
    {
        return _messageManager.GetMessageAsSender(agent);
    }

    public JObject GetMessageAsReceiver(GameObject agent)
    {
        return _messageManager.GetMessageAsReceiver(agent);
    }

    /// <summary>
    /// 获取Agent可见的所有Tag为"Visible"GameObject
    /// 注意这里非透明的物体一定要设置Collider碰撞组件
    /// </summary>
    /// <param name="agent">观察世界的Agent</param>
    /// <returns>能观察到的物体的列表</returns>
    private List<GameObject> GetVisiableObject(GameObject agent)
    {
        //获取当前场景中的所有Tag为"Visible"GameObject
        GameObject[] gameObjects = GameObject.FindGameObjectsWithTag("Visible");
        //定义可视物品列表
        List<GameObject> visibleGameObjects=new List<GameObject>();
        for (int i = 0; i < gameObjects.Length; i++)
        {
            GameObject target = gameObjects[i];
            var position = agent.transform.position;
            Ray ray=new Ray(position,target.transform.position-position);
            //定义一个光线投射碰撞 
            RaycastHit hit;
            //TODO:这里射线最大长度要超过地图对角线长度，有待敲定
            Physics.Raycast(ray, out hit, 100000);
            //如果没有碰撞
            if (hit.transform == null)
            {
                //加入可视物品列表
                visibleGameObjects.Add(target);
            }
        }
        return visibleGameObjects;
    }
    
    /// <summary>
    /// 获取Agent可见的所有Tag为"Visible"GameObject
    /// </summary>
    /// <param name="agent">观察世界的Agent</param>
    /// <returns>能观察到的物体的EnvMessage(Json格式string)</returns>
    public string GetVisiableObjectAsMessage(GameObject agent)
    {
        List<GameObject> visibleGameObjects=GetVisiableObject(agent);
        List<VisualMessage> visualMessages=new List<VisualMessage>();
        foreach(GameObject gameObject in visibleGameObjects)
        {
            var position = gameObject.transform.position;
            visualMessages.Add(new VisualMessage(""+position.x+position.y+position.z,gameObject.name));
        }
        return JsonConvert.SerializeObject(visualMessages);
    }


}
/// <summary>
/// immutable
/// 保存视觉信息，便于序列化
/// </summary>
class VisualMessage
{
    private readonly string pos;
    private readonly string objectName;

    public VisualMessage(string pos, string objectName)
    {
        this.pos = pos;
        this.objectName = objectName;
    }
}

/// <summary>
/// 听觉信息
/// </summary>
class HearingMessage
{
    //声音的大致方向
    private readonly AngelPire direction;
    //声音内容
    private readonly string content;

    public HearingMessage(AngelPire direction, string content)
    {
        this.direction = direction;
        this.content = content;
    }
}

/// <summary>
/// 声源方向角度对，在真实值两侧取随机误差
/// </summary>
class AngelPire
{
    private readonly float angel1;
    private readonly float angel2;

    public AngelPire(float angel1, float angel2)
    {
        this.angel1 = angel1;
        this.angel2 = angel2;
    }
}
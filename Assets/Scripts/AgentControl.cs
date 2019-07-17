using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using Newtonsoft.Json.Linq;
using Random = System.Random;

public class AgentControl : MonoBehaviour
{
    //IO对象
    private IOConcrete _ioConcrete;
    //Agent id，禁止在代码中修改
    [SerializeField]
    private string id="Adam";
    //待执行命令列表
    private readonly Queue<JObject> _nextOrder = new Queue<JObject>();

    //Agent状态
    private string _state;
    /// <summary>
    /// 返回Agent的ID
    /// </summary>
    /// <returns>返回Agent的ID</returns>
    public string GetID()
    {
        return id;
    }

    /// <summary>
    /// 向待执行命令队尾添加一个命令
    /// </summary>
    /// <param name="order">要添加的命令</param>
    public void AppendNextOrder(JObject order)
    {
        _nextOrder.Enqueue(order);
    }

    /// <summary>
    /// 向待执行命令队尾添加一组命令
    /// </summary>
    /// <param name="order">要添加的命令</param>
    public void AppendNextrOrder(List<JObject> order)
    {
        foreach(JObject jObject in order)
        {
            _nextOrder.Enqueue(jObject);
        }
    }


    // Start is called before the first frame update
    /// <summary>
    /// 初始化IO对象
    /// </summary>
    void Start()
    {
        _ioConcrete=gameObject.GetComponent<IOConcrete>();
        _ioConcrete.GetAgentControlOrder();
    }

    // Update is called once per frame
    void Update()
    {
        //获取本帧更新的所有命令
        List<JObject> orderList = _ioConcrete.GetAgentControlOrder();
        //与当前待执行的命令合并
        foreach (JObject jObject in orderList)
        {
            _nextOrder.Enqueue(jObject);
        }
        //执行命令
        DealOrder(_nextOrder.ToList());
    }
    /// <summary>
    /// 向别人发出请求获得某物
    /// 当前agent向目标agent发出请求，目标agent接收消息。
    /// 消息格式
    /// 参见passive order
    /// </summary>
    /// <param name="jObject">命令</param>
    private void Fun1(JObject jObject)
    {
        //获取target和agent的名字
        string targetName = jObject["param1"].ToString();
        string agentName = jObject["param2"].ToString();
        //获取游戏对象
        GameObject target = GameObject.Find(targetName);
        GameObject agent =  GameObject.Find(agentName);
        //获取脚本组件
        AgentControl agentControl = agent.GetComponent<AgentControl>();
        //向Agent发送请求
        //TODO    
        JObject message = JObject.Parse("{\"");
        agentControl.ReceiveMessage(message);
    }

    /// <summary>
    /// 使agent睡觉，播放sleep相关的动画
    /// agent躺下
    /// 设置agent的状态为"sleep"
    /// 睡觉过程中("sleep"状态下)agent不能hear和observe
    /// </summary>
    private void Sleep()
    {
        _state = "sleep";
        Animator agentAnimator = transform.GetComponent<Animator>();
        //设置为单次播放
        agentAnimator.SetBool("loop",false);
        //播放躺下的动画
        agentAnimator.Play("layDown");
        //设置为循环播放
        agentAnimator.SetBool("loop",true);
        //播放动画
        agentAnimator.Play("sleep");
    }
    
    /// <summary>
    /// 捕鱼
    /// 播放捕鱼的动画
    /// 有一定概率成功
    /// 播放对应成功/失败的动画
    /// 若成功，agent获得资源鱼
    /// TODO:GUI ?
    /// </summary>
    private void CatchFish()
    {
        //成功概率，百分制
        const int successFactor = 50;
        Animator agentAnimator = transform.GetComponent<Animator>();
        //设置为单次播放
        agentAnimator.SetBool("loop",false);
        //播放动画
        agentAnimator.Play("startCatchFish");
        //随机决定是否成功捕到鱼
        int val = new Random().Next(100);
        //成功
        agentAnimator.Play(val <= successFactor ? "succeedCatchFish" : "failedCatchFish");
    }
    
    /// <summary>
    /// 摘东西，只需要播放摘东西的动画本身，伸手的动画由其他方法完成
    /// 根据被摘取的东西播放相应的动画（通过动画命名控制）
    /// </summary>
    /// <param name="target">被摘取的东西</param>
    private void Pick(string target)
    {
        //处理target，确保其形式为首字母大写，其他小写
        target = target.Substring(0, 1).ToUpper() + target.Substring(1).ToLower();
        Animator agentAnimator = transform.GetComponent<Animator>();
        //设置为单次播放
        agentAnimator.SetBool("loop",false);
        //agentAnimator.wrapMode = WrapMode.Once;
        //播放动画
        agentAnimator.Play("pick"+target);
    }
    
    /// <summary>
    /// 吃东西，播放吃东西的动画
    /// </summary>
    /// <param name="target">被吃的东西，动画需要对应</param>
    /// <param name="speed">吃东西的速度，[0,5]的整数，影响动画播放速度，约定3为正常速度</param>
    private void Eat(string target,int speed)
    {
        float innerSpeed = 1;
        switch (speed)
        {
            case 0:
                innerSpeed = 0.25f;
                break;
            case 1:
                innerSpeed = 0.5f;
                break;
            case 2:
                innerSpeed = 0.75f;
                break;
            case 3:
                innerSpeed = 1f;
                break;
            case 4:
                innerSpeed = 1.5f;
                break;
            case 5:
                innerSpeed = 2f;
                break;
        }
        //处理target，确保其形式为首字母大写，其他小写
        target = target.Substring(0, 1).ToUpper() + target.Substring(1).ToLower();
        Animator agentAnimator = transform.GetComponent<Animator>();
        //设置为单次播放
        agentAnimator.SetBool("loop",false);
        //设置吃东西的速度
        agentAnimator.speed=innerSpeed;
        //播放动画
        agentAnimator.Play("eat"+target);
    }

    /// <summary>
    /// 使用工具收集雨水
    /// 执行后会播放放置工具的动画，并将工具实际放置在要求的位置
    /// </summary>
    /// <param name="toolName">工具名称</param>
    /// <param name="x">x坐标</param>
    /// <param name="y">y坐标</param>
    /// <param name="z">z坐标</param>
    private void CollectRainWater(string toolName,float x,float y,float z)
    {
        //TODO:xyz坐标是local还是global
        //TODO:明确Y轴表示上下,X轴表示左右，Z轴表示前后
        
        GameObject tool = GameObject.Find(toolName);
        //处理target，确保其形式为首字母大写，其他小写
        toolName = toolName.Substring(0, 1).ToUpper() + toolName.Substring(1).ToLower();
        Vector3 position=new Vector3(x,y,z);
        //播放动画
        Animator agentAnimator = transform.GetComponent<Animator>();
        AnimatorStateInfo info = agentAnimator.GetCurrentAnimatorStateInfo(0);
        //设置为单次播放
        agentAnimator.SetBool("loop",false);
        //播放动画
        agentAnimator.Play("collectRainWater"+toolName);
        //等待动画播放完成
        while (info.normalizedTime < 1.0f)
        {
            info = agentAnimator.GetCurrentAnimatorStateInfo(0);
        }
        //放置工具收集雨水
        tool.transform.Translate(position);
    }

    /// <summary>
    /// 播放取水动画（一瞬间）
    /// 转向取水坐标，取水，转回
    /// </summary>
    /// <param name="toolName"></param>
    /// <param name="x"></param>
    /// <param name="y"></param>
    /// <param name="z"></param>
    private void FetchWater(string toolName,float x,float y,float z)
    {
        //TODO:xyz坐标是local还是global
        //TODO:明确Y轴表示上下,X轴表示左右，Z轴表示前后
        //TODO:通知CBZ，此函数需要转向取水坐标，取水，转回
        GameObject tool = GameObject.Find(toolName);
        //处理target，确保其形式为首字母大写，其他小写
        toolName = toolName.Substring(0, 1).ToUpper() + toolName.Substring(1).ToLower();
        Quaternion faceDirectionBackUp = transform.rotation;
        //转动Agent
        transform.LookAt(new Vector3(x,y,z));
        //动画
        Animator agentAnimator = transform.GetComponent<Animator>();
        AnimatorStateInfo info = agentAnimator.GetCurrentAnimatorStateInfo(0);
        //设置为单次播放
        agentAnimator.SetBool("loop",false);
        //播放动画
        agentAnimator.Play("fetchWater"+toolName);
        //等待动画播放完成
        while (info.normalizedTime < 1.0f)
        {
            info = agentAnimator.GetCurrentAnimatorStateInfo(0);
        }
        //把Agent转回来
        transform.LookAt(faceDirectionBackUp.eulerAngles);
    }
    
    /// <summary>
    ///喝饮料，播放喝饮料的动画
    /// </summary>
    /// <param name="target">被喝的饮料种类，动画需要对应</param>
    /// <param name="speed">喝饮料的速度，[0,5]的整数，影响动画播放速度，约定3为正常速度</param>
    private void Drink(string target,int speed)
    {
        //TODO:对吃喝东西的速度的定义
        float innerSpeed = 1;
        switch (speed)
        {
            case 0:
                innerSpeed = 0.25f;
                break;
            case 1:
                innerSpeed = 0.5f;
                break;
            case 2:
                innerSpeed = 0.75f;
                break;
            case 3:
                innerSpeed = 1f;
                break;
            case 4:
                innerSpeed = 1.5f;
                break;
            case 5:
                innerSpeed = 2f;
                break;
        }
        //处理target，确保其形式为首字母大写，其他小写
        target = target.Substring(0, 1).ToUpper() + target.Substring(1).ToLower();
        Animator agentAnimator = transform.GetComponent<Animator>();
        //设置为单次播放
        agentAnimator.SetBool("loop",false);
        //设置吃东西的速度
        agentAnimator.speed=innerSpeed;
        //播放动画
        agentAnimator.Play("drink"+target);
    }
    
    private void Fun1Passive(JObject jObject)
    {
        //获取target和agent的名字
        string targetName = jObject["param1"].ToString();
        string agentName = jObject["param2"].ToString();
        //获取游戏对象
        GameObject target = GameObject.Find(targetName);
        GameObject agent =  GameObject.Find(agentName);
        //获取脚本组件
        AgentControl agentControl = agent.GetComponent<AgentControl>();
    }
    
    /// <summary>
    /// 执行收到的指令
    /// </summary>
    /// <param name="list">指令列表</param>
    private void DealOrder(List<JObject> list)
    {
        foreach (JObject jObject in list)
        {
            string function = jObject["operation"].ToString();
            switch (function)
            {
                case "func1":
                    Fun1(jObject);
                    break;
                case "func2":
                    break;
                case "func3":
                    break;
                case "func4":
                    break;
                case "func5":
                    break;
                case "func6":
                    break;
                case "func7":
                    break;
                case "func8":
                    break;
                case "sleep":
                    Sleep();
                    break;
                case "catchfish":
                    CatchFish();
                    break;
                case "pick":
                    Pick(jObject["param1"].ToString());
                    break;
                case "eat":
                    Eat(jObject["param1"].ToString(),int.Parse(jObject["param2"].ToString()));
                    break;
                case "drink":
                    Drink(jObject["param1"].ToString(),int.Parse(jObject["param2"].ToString()));
                    break;
                case "collect_rainwater":
                    CollectRainWater(jObject["param1"].ToString(),float.Parse(jObject["param2"].ToString()),float.Parse(jObject["param3"].ToString()),float.Parse(jObject["param4"].ToString()));
                    break;
                case "fetch_water":
                    FetchWater(jObject["param1"].ToString(),float.Parse(jObject["param2"].ToString()),float.Parse(jObject["param3"].ToString()),float.Parse(jObject["param4"].ToString()));
                    break;
                
            }
        }
    }
    public void ReceiveMessage(JObject jObject)
    {
        string function = jObject["operation"].ToString();
        switch (function)
        {
            case "func1_passive":
                
                break;
            case "func2_passive":
                break;
            case "func3_passive":
                break;
            case "func4_passive":
                break;
            case "func5_passive":
                break;
            case "func6_passive":
                break;
            case "func7_passive":
                break;
            case "func8_passive":
                break;

        }
    }
    
    
}

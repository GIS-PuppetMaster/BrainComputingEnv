using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Ball : MonoBehaviour
{
    void OnBecameInvisible()
    {
        Destroy(this.gameObject);
    }
    // Start is called before the first frame update
    void Start()
    {
         //this.GetComponent<Rigidbody>().velocity = new Vector3(-5.0f, 5.0f, 0.0f); //设置向左上方的速度
        
    }

    // Update is called once per frame
    void Update()
    {
    }
}

using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEngine;
using UnityEngine.UI;
public class TextControl : MonoBehaviour
{
    public Text UItext;
    static private readonly string path = "C://Users//zkx74//Desktop//totalTest//database//output.txt";
    
    // Start is called before the first frame update
    void Start()
    {
        UItext = GetComponent<Text>();
    }

    // Update is called once per frame
    void Update()
    {
        string output = File.ReadAllText(path, Encoding.UTF8);
        UItext.text = output;       
    }
}

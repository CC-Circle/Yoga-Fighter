using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Goal : MonoBehaviour
{
    [SerializeField] private int goal;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
        //Debug.Log(set_segment.top_position.y);
        if(set_segment.top_position.y >= goal) {
            // Debug.Log("これ"+set_segment.top_position.y);
            // Debug.Log("hogehoge");
            SceneManager.LoadScene("Goal");
        }
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class camera_follo : MonoBehaviour
{


    float count_x;
    // Start is called before the first frame update
    void Start()
    {
        //count_x = transform.position.x;
    }

    // Update is called once per frame
    void Update()
    {


        //if (Input.GetKey(KeyCode.Space))
        //{
            transform.position = new Vector3(0f, set_segment.top_position.y + 3f, set_segment.top_position.z - 5f);
        //}
    }
}

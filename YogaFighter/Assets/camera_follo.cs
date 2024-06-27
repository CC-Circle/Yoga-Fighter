using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class camera_follo : MonoBehaviour
{


    float count_x;
    // Start is called before the first frame update
    void Start()
    {
        count_x = transform.position.x;
    }

    // Update is called once per frame
    void Update()
    {

        if (Input.GetKey(KeyCode.LeftArrow))
        {
            count_x -= 0.01f;
        }
        if (Input.GetKey(KeyCode.RightArrow))
        {
            count_x += 0.01f;
        }


        if (Input.GetKey(KeyCode.Space))
        {
            transform.position = new Vector3(count_x, transform.position.y + 0.1f, transform.position.z);
        }
    }
}

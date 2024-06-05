using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class enem_move : MonoBehaviour
{
    Transform objectTransform;
    float movementDistance;

    float targetScale = 3.4f; // Desired final scale (relative to initial scale)
    float scalingSpeed = 0.1f; // Amount to scale per update (e.g., 0.1 units per frame)
    float timeInterval = 0.01f; // Time interval between scaling updates (in seconds)

    // Start is called before the first frame update
    void Start()
    {
        objectTransform = gameObject.transform;

        // Define the movement distance
        movementDistance = 0.01f; // Adjust this value as needed

    }

    // Update is called once per frame
    void Update()
    {
        if(transform.position.z < 0)
        {
            Destroy(this.gameObject);
        }
        objectTransform.Translate(Vector3.back * movementDistance);

        scalingSpeed = 1 / transform.position.z;


        if (objectTransform.localScale.magnitude < targetScale)
        {
            objectTransform.localScale += Vector3.one * scalingSpeed * Time.deltaTime;

            // Clamp scale to prevent exceeding target scale
            objectTransform.localScale = Vector3.ClampMagnitude(objectTransform.localScale, targetScale);
        }

    }


}

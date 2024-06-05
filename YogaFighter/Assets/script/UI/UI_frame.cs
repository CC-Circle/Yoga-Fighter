using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.UI;
using UnityEngine.UI;

public class UI_frame : MonoBehaviour
{

    public GameObject frame2;
    public GameObject frame1;

    public GameObject pose1;
    public GameObject pose2;
    public GameObject pose3;

    public GameObject ele1;
    public GameObject ele2;
    public GameObject ele3;

    public int mode = -1;//0 縦 1 横 2 L
    public int Side = 1;//横
    public int Height = 0;//高さ
    public int now_ele = -1;
    public int tue_Side = 1;


    RectTransform rectTransform_f1;
    RectTransform rectTransform_f2;
    // Start is called before the first frame update
    void Start()
    {
        rectTransform_f1 = frame1.GetComponent<RectTransform>();
        rectTransform_f2 = frame2.GetComponent<RectTransform>();
    }

    // Update is called once per frame
    void Update()
    {

        if (Input.GetKeyDown(KeyCode.I))
        {
            mode = 0;
        }
        else if (Input.GetKeyDown(KeyCode.O))
        {
            mode = 1;
        }
        else if (Input.GetKeyDown(KeyCode.P))
        {
            mode = 2;
        }
        else if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            if (Height < 2)
            {
                Height++;
            }
        }
        else if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            if (Height > 0)
            {
                Height--;
            }
        }
        else if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            if (Side > 0)
            {
                Side--;
            }
            tue_Side = 0;
        }
        else if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            if (Side < 2)
            {
                Side++;
            }
            tue_Side = 1;
        }
        else if (Input.GetKeyDown(KeyCode.Q))
        {
            now_ele = 0;
        }
        else if (Input.GetKeyDown(KeyCode.W))
        {
            now_ele = 1;
        }
        else if (Input.GetKeyDown(KeyCode.E))
        {
            now_ele = 2;
        }


        if (Input.anyKeyDown)
        {
            Flame_draw();
            ele_draw();
        }
    }

    void ele_draw()
    {
        if(now_ele == 0)
        {
            if (!ele1.active)
            {
                ele1.SetActive(true);
                ele2.SetActive(false);
                ele3.SetActive(false);

                for (int i = 0; i < 6; i++)
                {
                    Transform childTransform1 = frame1.transform.GetChild(i);
                    Transform childTransform2 = frame2.transform.GetChild(i);


                    // 子要素にアクセス
                    childTransform1.GetComponent<Image>().color = new Color(1.0f, 0.0f, 0.0f);
                    childTransform2.GetComponent<Image>().color = new Color(1.0f, 0.0f, 0.0f);
                    
                }
            }
        }else if(now_ele == 1)
        {
            if (!ele2.active)
            {
                ele1.SetActive(false);
                ele2.SetActive(true);
                ele3.SetActive(false);

                for (int i = 0; i < 6; i++)
                {
                    Transform childTransform1 = frame1.transform.GetChild(i);
                    Transform childTransform2 = frame2.transform.GetChild(i);


                    // 子要素にアクセス
                    childTransform1.GetComponent<Image>().color = new Color(0.0f, 1.0f, 0.0f);
                    childTransform2.GetComponent<Image>().color = new Color(0.0f, 1.0f, 0.0f);

                }
            }
        }else if(now_ele == 2)
        {
            if (!ele3.active)
            {
                ele1.SetActive(false);
                ele2.SetActive(false);
                ele3.SetActive(true);

                for (int i = 0; i < 6; i++)
                {
                    Transform childTransform1 = frame1.transform.GetChild(i);
                    Transform childTransform2 = frame2.transform.GetChild(i);


                    // 子要素にアクセス
                    childTransform1.GetComponent<Image>().color = new Color(0.0f, 0.0f, 1.0f);
                    childTransform2.GetComponent<Image>().color = new Color(0.0f, 0.0f, 1.0f);

                }
            }
        }
    }

    void Flame_draw()
    {

        if(mode == 0)
        {
            if (!frame1.active)
            {
                frame1.SetActive(true);
            }
            if (frame2.active)
            {
                frame2.SetActive(false);
            }

            if (!pose1.active)
            {
                pose1.SetActive(true);
                pose2.SetActive(false);
                pose3.SetActive(false);
            }

            Vector3 targetPosition = new Vector3(-150, 500 * Height, 1);

            // localPositionをtargetPositionに更新
            rectTransform_f1.localPosition = targetPosition;
        }
        if (mode == 1)
        {
            if (!frame2.active)
            {
                frame2.SetActive(true);
            }
            if (frame1.active)
            {
                frame1.SetActive(false);
            }
            Vector3 targetPosition = new Vector3(500 * (Side-1), -50, 1);

            // localPositionをtargetPositionに更新
            rectTransform_f2.localPosition = targetPosition;
            if (!pose2.active)
            {
                pose1.SetActive(false);
                pose2.SetActive(true);
                pose3.SetActive(false);
            }
        }
        if (mode == 2)
        {
            if (!frame1.active | !frame2.active)
            {
                frame1.SetActive(true);
                frame2.SetActive(true);
            }
            Vector3 targetPosition = new Vector3(-150, 0, 1);

            // localPositionをtargetPositionに更新
            rectTransform_f1.localPosition = targetPosition;

            targetPosition = new Vector3(-500 + 1000 *(tue_Side), -50, 1);

            // localPositionをtargetPositionに更新
            rectTransform_f2.localPosition = targetPosition;
            if (!pose3.active)
            {
                pose1.SetActive(false);
                pose2.SetActive(false);
                pose3.SetActive(true);
            }
        }
    }
}

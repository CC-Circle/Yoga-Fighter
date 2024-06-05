using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Gage_mana : MonoBehaviour
{
    public Slider slider;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        slider.value += Time.deltaTime * 0.01f; // 毎フレームスライダーの値を0.1ずつ増加
        if (slider.value >= 1f)
        {
            slider.value = 1f; // スライダーの値が1を超えたら1に固定
        }
    }
}

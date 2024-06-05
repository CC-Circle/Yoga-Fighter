using UnityEngine;
using System.IO;


public class Input_csv : MonoBehaviour
{
    public GameObject enem;
    public GameObject camera;

    // Start メソッド内で CSV ファイルを読み込みます
    void Start()
    {
        // Resources フォルダから "data.csv" という名前で CSV ファイルを読み込む
        TextAsset csvData = Resources.Load("data") as TextAsset;

        // CSV データを解析
        if (csvData != null)
        {
            StringReader reader = new StringReader(csvData.text);
            int count = 0;
            while (true)
            {
                string line = reader.ReadLine();
                if (line == null) break;

                // カンマ区切りで分割
                string[] values = line.Split(',');

                // 各値を処理
                for (int i = 0; i < values.Length; i++)
                {
                    //Debug.Log(values[i] +","+count);
                    int value = int.Parse(values[i]);
                    if( value != 0)
                    {
                        float x = value % 3;
                        switch (x)
                        {
                            case 0:
                                x = 2;
                                break;
                            case 1:
                                x = 0;
                                break;
                            case 2:
                                x = 1;
                                break;
                        }
                        float y = value / 3;
                        if(value%3 != 0)
                        {
                            y++;
                        }

                        Vector3 position = new Vector3(-3.6f + 2.78f*x , -2.0f + 2.7f*(y-1), 6f*count+4f);
                        Quaternion spawnRotation = Quaternion.Euler(0, 0, 0);
                        GameObject instance = Instantiate(enem, position,spawnRotation);
                        instance.transform.parent = camera.transform;
                    }
                }
                count++;
            }
        }
        else
        {
            Debug.LogError("CSV ファイルを読み込めませんでした。");
        }
    }
}
///// 1 2 3
///// 4 5 6
///// 7 8 9
using UnityEngine;

public class nobiru_cube : MonoBehaviour
{
    float growthSpeed = 2.0f; // 1秒あたりの成長量
    float growthLimit; // 最大成長高さ
    float growadd = 1.0f;
    float growthAngle = 30.0f; // 成長の角度 (X軸正方向からの傾き角度)


    private Mesh mesh;
    private Vector3[] vertices;
    float currentHeight = 0.0f; // 現在の高さ
    private static float growthDirection = 0.0f; // X軸方向の成長方向 (0: 真上, 1: 正方向, -1: 負方向)


    [SerializeField] float left_limit = -2.0f;
    [SerializeField] float right_limit = 2.0f;

    void Start()
    {
        mesh = GetComponent<MeshFilter>().mesh;
        vertices = mesh.vertices;
        
        growthLimit = growadd;
    }

    void Update()
    {
        // 成長が最大高さに達していない場合
        if (currentHeight < growthLimit)
        {
            // 十字キー入力による成長方向の制御
            if (Input.GetKey(KeyCode.RightArrow))
            {

                if (set_segment.top_position.x < right_limit)
                {
                    growthDirection = 1.0f;
                }
                else
                {
                    growthDirection = 0.0f;
                }
                

            }
            else if (Input.GetKey(KeyCode.LeftArrow))
            {

                if (set_segment.top_position.x > left_limit)
                {
                    growthDirection = -1.0f;
                }
                else
                {
                    growthDirection = 0.0f;
                }
                
            }
            else
            {
                //growthDirection = 0.0f;

                if (set_segment.top_position.x > right_limit)
                {
                    growthDirection = 0.0f;
                }

                if (set_segment.top_position.x < left_limit)
                {
                    growthDirection = 0.0f;
                }
            }



            // Y軸方向に頂点を移動
            for (int i = 0; i < vertices.Length; i++)
            {
                // Y座標が現在の高さより低い頂点はそのまま
                if (vertices[i].y <= currentHeight)
                {
                    continue;
                }

                // Y座標が現在の高さより高い頂点は、上に移動し、X方向にも移動
                float yOffset = vertices[i].y - currentHeight;
                float xOffset = yOffset * Mathf.Tan(growthAngle * Mathf.Deg2Rad);
                


                // X方向の移動方向を調整
                if (growthDirection > 0.0f)
                {
                    vertices[i].x += xOffset * Time.deltaTime;

                }
                else if (growthDirection < 0.0f)
                {
                    vertices[i].x -= xOffset * Time.deltaTime;
                }
                
                vertices[i].y += growthSpeed * Time.deltaTime;
            }

            // 現在の高さを更新
            currentHeight += growthSpeed * Time.deltaTime;

            // メッシュの更新
            mesh.vertices = vertices;
        }
    }
}

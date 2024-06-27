using UnityEngine;

public class nobiru_branch : MonoBehaviour
{
    float growthSpeed = 1.0f; // 1秒あたりの成長量
    float growthLimit; // 最大成長高さ
    float growadd = 0.5f;
    

    private Mesh mesh;
    private Vector3[] vertices;
    float currentHeight = 0.0f; // 現在の高さ
    private static float growthDirection = 0.0f; // X軸方向の成長方向 (0: 真上, 1: 正方向, -1: 負方向)

    public GameObject nobiru_branch_obj;
    GameObject obj2;
    public GameObject pre_obj2;

    bool is_end = false;

    float angle = -90f;

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
                
                vertices[i].y += growthSpeed * Time.deltaTime;
            }

            // 現在の高さを更新
            currentHeight += growthSpeed * Time.deltaTime;

            // メッシュの更新
            mesh.vertices = vertices;


        }else if(is_end == false)
        {
            Vector3 desiredRotation = new Vector3(angle, 0f, 0f);
            if (pre_obj2 != null)
            {
                Debug.Log("ok");
                Vector3 top_mesh = GetTopPosition(pre_obj2);
                obj2 = Instantiate(nobiru_branch_obj, new Vector3(top_mesh.x - 0.25f, top_mesh.y - 0.25f, top_mesh.z), Quaternion.identity);

            }
            else
            {
                obj2 = Instantiate(nobiru_branch_obj, new Vector3(transform.position.x, transform.position.y, transform.position.z), Quaternion.identity);

            }

            is_end = true;
            Debug.Log(transform.rotation.x);
            
            // Quaternion.Euler を使って回転角度を指定
            obj2.transform.rotation = Quaternion.Euler(desiredRotation);
            obj2.GetComponent<nobiru_branch>().angle = angle / 1.01f;
            obj2.GetComponent<nobiru_branch>().pre_obj2 = this.gameObject;
        }
    }

    Vector3 GetTopPosition(GameObject in_obj)
    {
        Vector3 topPosition = Vector3.zero;
        float maxY = float.MinValue;

        mesh = in_obj.GetComponent<MeshFilter>().mesh;
        vertices = mesh.vertices;

        // 最高点の頂点を探す
        foreach (var vertex in vertices)
        {
            if (vertex.y > maxY)
            {
                maxY = vertex.y;
                topPosition = in_obj.transform.TransformPoint(vertex); // ローカル座標からワールド座標に変換
            }
        }

        return topPosition;
    }
}

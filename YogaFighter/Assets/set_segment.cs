using UnityEngine;
using System.Collections;

public class set_segment : MonoBehaviour
{

    public GameObject cube_obj;
    public GameObject branch_obj;
    public GameObject branch_obj2;
    float add_value = 0.29f;

    public static Vector3 top_position;

    private Vector3[] vertices;
    private Mesh mesh;

    GameObject obj;
    GameObject obj2;
    GameObject obj3;

    private Vector3 next_position;

    int branch_count = 0;

    void Start()
    {
        obj = Instantiate(cube_obj, new Vector3(0,0,0), Quaternion.identity);

        // コルーチンを開始
        StartCoroutine(RepeatedCoroutine());
    }

    private void Update()
    {
        GetTopPosition(obj);
    }

    IEnumerator RepeatedCoroutine()
    {
        float y_value = 0;
        while (true)
        {
            
            // ここに秒ごとに実行する処理を書く
            yield return new WaitForSeconds(0.5f);  // 1秒待機

            next_position = GetTopPosition(obj);
            Debug.Log(next_position);


            y_value += add_value;
            obj = Instantiate(cube_obj, new Vector3(next_position.x+0.475f, transform.position.y + y_value, transform.position.z), Quaternion.identity);

            branch_count++;
            if(branch_count %5 == 0)
            {
                Vector3 desiredRotation = new Vector3(-90f, 0f, 0f);
                //obj2 = Instantiate(branch_obj, new Vector3(next_position.x - 0.5f, transform.position.y + y_value - 0.2f, transform.position.z-0.5f), Quaternion.identity);
                // Quaternion.Euler を使って回転角度を指定
                //obj2.transform.rotation = Quaternion.Euler(desiredRotation);


                desiredRotation = new Vector3(90f, 0f, 0f);
                //obj3 = Instantiate(branch_obj2, new Vector3(next_position.x - 0.5f, transform.position.y + y_value - 0.2f, transform.position.z+0.5f), Quaternion.identity);
                // Quaternion.Euler を使って回転角度を指定
                //obj3.transform.rotation = Quaternion.Euler(desiredRotation);


            }
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

        top_position = topPosition;
        top_position.x = topPosition.x + 0.475f;
        return topPosition;
    }
}

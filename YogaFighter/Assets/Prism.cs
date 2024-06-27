using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Prism : MonoBehaviour
{
    public int n = 6;// 正n角形のn
    void Start()
    {
        MeshFilter meshFilter = gameObject.GetComponent<MeshFilter>();// メッシュフィルター
        MeshRenderer meshRenderer = gameObject.GetComponent<MeshRenderer>();// メッシュレンダラー
        MeshCollider meshCollider = gameObject.GetComponent<MeshCollider>();// メッシュコライダー
        Mesh mesh = new Mesh();// メッシュ
        Vector3[] vertices = new Vector3[n * 6];// メッシュの頂点座標
        int[] triangles = new int[(n - 1) * 12];// メッシュの三角形情報
        for (int i = 0; i < n; i++)
        {
            // 底面の頂点
            vertices[i] = (Quaternion.Euler(0, 0, (360f / n) * i) * Vector3.up) + Vector3.back * 0.5f;
            vertices[n + i] = vertices[i] + Vector3.forward;
        }
        for (int i = 0; i < n; i++)
        {
            // 側面の頂点
            vertices[n * 2 + i * 4 + 0] = vertices[0 + i];
            vertices[n * 2 + i * 4 + 1] = vertices[(1 + i) % n];
            vertices[n * 2 + i * 4 + 2] = vertices[n + (1 + i) % n];
            vertices[n * 2 + i * 4 + 3] = vertices[n + i];
        }
        for (int i = 0; i < n - 2; i++)
        {
            // 手前の底面
            triangles[i * 3 + 0] = 0;
            triangles[i * 3 + 1] = 2 + i;
            triangles[i * 3 + 2] = 1 + i;
            // 奥の底面
            triangles[(n - 2) * 3 + i * 3 + 0] = n;
            triangles[(n - 2) * 3 + i * 3 + 1] = n + 1 + i;
            triangles[(n - 2) * 3 + i * 3 + 2] = n + 2 + i;
        }// ~ (n-2)*6
        for (int i = 0; i < n; i++)
        {
            // i番目の側面
            triangles[(n - 2) * 6 + i * 6 + 0] = n * 2 + i * 4 + 0;
            triangles[(n - 2) * 6 + i * 6 + 1] = n * 2 + i * 4 + 1;
            triangles[(n - 2) * 6 + i * 6 + 2] = n * 2 + i * 4 + 2;
            triangles[(n - 2) * 6 + i * 6 + 3] = n * 2 + i * 4 + 2;
            triangles[(n - 2) * 6 + i * 6 + 4] = n * 2 + i * 4 + 3;
            triangles[(n - 2) * 6 + i * 6 + 5] = n * 2 + i * 4 + 0;
        }// ~ (n-1)*12
        mesh.SetVertices(vertices);// メッシュの頂点を設定
        mesh.SetTriangles(triangles, 0);// メッシュの三角形を設定
        mesh.RecalculateNormals();// 法線ベクトルの設定
        meshFilter.sharedMesh = mesh;// メッシュフィルターにメッシュを設定
        meshCollider.sharedMesh = mesh;// メッシュコライダーにメッシュを設定
    }
}

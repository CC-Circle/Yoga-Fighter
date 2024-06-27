using System.Linq;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class TubeExtension : MonoBehaviour
{
    public Vector3 extensionDirection = Vector3.up;
    public float extensionSpeed = 1.0f;

    private MeshFilter meshFilter;
    private List<Vector3> vertices = new List<Vector3>();
    private List<Vector2> uv = new List<Vector2>();
    private List<Vector3> prevVertices = new List<Vector3>();
    private List<Vector3> additionalVertices = new List<Vector3>();
    private List<Vector2> additionalUV = new List<Vector2>();

    private int segments = 16; // Declare segments as a field


    void Start()
    {
        meshFilter = GetComponent<MeshFilter>();
        vertices.AddRange(meshFilter.sharedMesh.vertices);
        uv.AddRange(meshFilter.sharedMesh.uv);

        if (uv.Count != vertices.Count)
        {
            Debug.LogError("エラー: uv 配列のサイズ (" + uv.Count + ") が vertices 配列のサイズ (" + vertices.Count + ") と一致しません。");
            return;
        }

        CreateAdditionalVertices();
        CreateAdditionalUV();
    }

    void Update()
    {
        List<Vector3> newVertices = new List<Vector3>();

        for (int i = 0; i < vertices.Count; i++)
        {
            vertices[i] += extensionDirection * extensionSpeed * Time.deltaTime;
            newVertices.Add(vertices[i]);
        }

        Vector3 lastVertex = vertices[vertices.Count - 1];
        Vector3 newVertex = lastVertex + extensionDirection * extensionSpeed;
        newVertices.Add(newVertex);

        UpdateAdditionalVertices();

        meshFilter.mesh.vertices = newVertices.ToArray();
        meshFilter.mesh.uv = (uv.ToArray() as Vector2[]).Concat(additionalUV.ToArray()).ToArray();
        meshFilter.mesh.RecalculateNormals();

        prevVertices.Clear();
        prevVertices.AddRange(vertices);
    }

    private void CreateAdditionalVertices()
    {
        float radius = 0.5f;
        int segments = 16; // Declare segments within the function

        for (int i = 0; i <= segments; i++)
        {
            float angle = (i / (float)segments) * Mathf.PI * 2.0f;
            Vector3 position = new Vector3(radius * Mathf.Cos(angle), radius * Mathf.Sin(angle), 0.0f);
            additionalVertices.Add(position);
        }
    }

    private void CreateAdditionalUV()
    {
        int segments = 16;
        
        for (int i = 0; i <= segments; i++)
        {
            float u = (float)i / (float)segments;
            float v = 1.0f;
            additionalUV.Add(new Vector2(u, v));
        }
        
    }

    private void UpdateAdditionalVertices()
    {
        Vector3 lastVertex = vertices[vertices.Count - 1];
        for (int i = 0; i < additionalVertices.Count; i++)
        {
            additionalVertices[i] = lastVertex + additionalVertices[i];
        }
    }
}

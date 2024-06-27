using UnityEngine;
using TreeEditor;

public class TreeManipulator : MonoBehaviour
{

    void Start()
    {
        // このゲームオブジェクトにアタッチされているすべてのコンポーネントを取得
        Component[] components = GetComponents<Component>();

        // コンポーネントの一覧をログに出力
        foreach (var component in components)
        {
            Debug.Log("Component: " + component.GetType().Name);
        }

        Tree tree_info = gameObject.GetComponent<Tree>();
        

        Debug.Log(tree_info.data);
        
    }

    void Update()
    {
        
    }

    
}

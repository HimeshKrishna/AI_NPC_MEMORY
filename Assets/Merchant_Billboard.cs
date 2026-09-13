using UnityEngine;

public class BillboardText : MonoBehaviour
{
    void Update()
    {
        transform.LookAt(Camera.main.transform);
        transform.Rotate(0,180,0);
    }
}
using UnityEngine;

public class SimpleCameraFollow : MonoBehaviour
{
    public Transform player;

    void LateUpdate()
    {
        Vector3 newPosition = player.position;

        newPosition.y = 6;      // camera height
        newPosition.z = player.position.z - 10;  // camera stays behind player

        transform.position = newPosition;
    }
}
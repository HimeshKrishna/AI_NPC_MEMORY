using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using TMPro;

public class AIDialogueManager : MonoBehaviour
{
    public TMP_Text dialogueText;

    public void AskNPC(string npcName, string message)
    {
        StartCoroutine(SendRequest(npcName, message));
    }

    IEnumerator SendRequest(string npc, string message)
    {
        string json = "{\"npc\":\"" + npc + "\",\"message\":\"" + message + "\"}";

        UnityWebRequest request = new UnityWebRequest("http://localhost:5000/npc", "POST");

        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(json);

        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();

        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            string jsonResponse = request.downloadHandler.text;

            NPCReply response = JsonUtility.FromJson<NPCReply>(jsonResponse);

            dialogueText.text = response.reply;
        }
        else
        {
            dialogueText.text = "Server Error.";
        }
    }
}

[System.Serializable]
public class NPCReply
{
    public string reply;
}

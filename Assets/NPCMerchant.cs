using UnityEngine;
using TMPro;
using System.Collections;

public class NPCMerchant : MonoBehaviour
{
    public AIDialogueManager aiManager;
    public string npcName = "Merchant";

    public Transform player;
    public float interactionDistance = 3f;

    public GameObject dialoguePanel;
    public TMP_Text dialogueText;

    private bool hasMetPlayer = false;

    void Start()
    {
        hasMetPlayer = PlayerPrefs.GetInt("MetMerchant", 0) == 1;
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.R))
        {
            PlayerPrefs.DeleteKey("MetMerchant");
            hasMetPlayer = false;

            Debug.Log("Merchant memory reset.");
        }

        float dist = Vector3.Distance(player.position, transform.position);

        if (dist < interactionDistance)
        {
            Vector3 direction = player.position - transform.position;
            direction.y = 0;
            transform.rotation = Quaternion.LookRotation(direction);

            if (Input.GetKeyDown(KeyCode.E))
            {
                dialoguePanel.SetActive(true);

                if (!hasMetPlayer)
                {
                    aiManager.AskNPC(npcName, "Hello, nice to meet you!");
                    hasMetPlayer = true;

                    PlayerPrefs.SetInt("MetMerchant", 1);
                    PlayerPrefs.Save();
                }
                else
                {
                    aiManager.AskNPC(npcName, "Nice to see you again!");
                }
            }
        }
    }
}
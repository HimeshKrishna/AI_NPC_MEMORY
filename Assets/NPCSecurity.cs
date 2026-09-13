using UnityEngine;
using TMPro;
using System.Collections;

public class NPCSecurity : MonoBehaviour
{
    public AIDialogueManager aiManager;
    public string npcName = "Guard";

    public Transform player;
    public float interactionDistance = 3f;

    public GameObject dialoguePanel;
    public TMP_Text dialogueText;

    private bool hasMetPlayer = false;

    void Start()
    {
        hasMetPlayer = PlayerPrefs.GetInt("MetGuard", 0) == 1;
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.R))
        {
            PlayerPrefs.DeleteKey("MetGuard");
            hasMetPlayer = false;

            Debug.Log("Guard memory reset.");
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
                    aiManager.AskNPC(npcName, "Halt. Who are you and why are you here?");
                    hasMetPlayer = true;

                    PlayerPrefs.SetInt("MetGuard", 1);
                    PlayerPrefs.Save();
                }
                else
                {
                    aiManager.AskNPC(npcName, "You're back again. What do you want this time?");
                }
            }
        }
    }
}
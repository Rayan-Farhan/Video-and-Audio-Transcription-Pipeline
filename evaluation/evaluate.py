import os
import json
import re
from typing import Dict, Any, List

def _normalize(s: str) -> List[str]:
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    return s.split()

def wer(ref: str, hyp: str) -> float:
    r = _normalize(ref)
    h = _normalize(hyp)
    n = len(r)
    m = len(h)
    d = [[0] * (m+1) for _ in range(n+1)]
    for i in range(n+1):
        d[i][0] = i
    for j in range(m+1):
        d[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = 1 + min(d[i-1][j], d[i][j-1], d[i-1][j-1])
    return d[n][m] / max(1, n)

def load_all_transcripts(json_dir: str) -> Dict[str, Any]:
    results = {}
    if not os.path.isdir(json_dir):
        raise FileNotFoundError(f"{json_dir} not found")
    for fname in os.listdir(json_dir):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(json_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            results[data['file_id']] = data
    return results

def evaluate(json_dir: str, references: Dict[str, str], save_report: str = "evaluation/report.json"):
    os.makedirs(os.path.dirname(save_report), exist_ok=True)
    transcripts = load_all_transcripts(json_dir)
    print(f"Loaded {len(transcripts)} transcripts from {json_dir}")
    report = {}

    for key, reference in references.items():
        entry = {"found": False}

        data = transcripts.get(key)

        if data is None:
            data = next((d for d in transcripts.values() if d["filename"] == key), None)

        if data:
            hyp_text = data.get("cleaned", {}).get("text") or data.get("raw", {}).get("text", "")
            latency = data.get("latency_seconds", None)
            score = wer(reference, hyp_text)
            entry.update({
                "found": True,
                "filename": data.get("filename"),
                "wer": score,
                "latency_seconds": latency,
                "reference": reference,
                "hypothesis": hyp_text
            })
        else:
            entry.update({"error": "transcript not found"})

        report[key] = entry

    with open(save_report, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    for fid, r in report.items():
        if r.get("found"):
            print(f"File {fid}: WER={r['wer']:.2%}, latency={r['latency_seconds']}s, filename={r['filename']}")
        else:
            print(f"File {fid}: NOT FOUND")

    print(f"\nSaved evaluation report to {save_report}")
    return report

references = {
    "test.mp4": "Hello all, my name is Krishna and welcome to my YouTube channel. So guys, I am super excited to announce our new Udemy course that is nothing but building AI agents and agentic AI systems with the help of Microsoft Autogen. Now if you don't know Microsoft Autogen is also one of the most popular framework that will be specifically used to develop agentic AI applications. uh now in the world of era wherein everybody's focusing on building AI agents in agentic AI system it is important that we have knowledge with respect to multiple frameworks and that is the reason me and my entire team are working really really hard to come up with some amazing courses in an affordable way wherein we cover all the specific frameworks in much more in depth I've already uploaded one course with respect to langraph now we are going to cover up with Microsoft autogen and uh the feedback back from all the specific courses has been quite amazing and people are really demanding for more and more different kind of use cases and uh different kind of implementation where we can develop agentic AI system such that we take it into the production level. So anybody who is specifically interested into getting into generative AI agentic AI then this is the course definitely for you. uh in this video I'll be talking more about this particular courses what all things you can you will be learning what are the prerequisites that you actually require in order to learn this and many more things okay so first of all uh here in this particular course uh this has been collaborated with Mayank Agarwal I hope everybody knows about Mayank Agarwal uh he is the part of my team where we are focusing on understanding what all things people definitely require to get into this specific industry right uh so here to go ahead with right now this particular course fees is only 3.99 rupees. Um and understand if you just need to use a coupon which is called as agentic01. Uh as I said the course price is very very minimal less than a Starbucks coffee and uh this entire course will be available for lifetime. You also have 30 days refund policy. So let's say you buy this particular course try out the videos and if you don't like it within 30 days you can also get the refund. What is the main aim in this particular course is to build powerful AI agents, automate task and create advanced agentic AI system. Since Microsoft autogen is from Microsoft itself. So definitely you can understand right what will be the importance of this particular framework. Right? because right now there are some less number of companies which are really really competitive in this market with respect to developing LLM models, frameworks and many more things and Microsoft have definitely come up with something autogen called as autogen for a specific purpose. So uh in this course you'll learn all about what are agents, how to create autonomous agents, how to interact with the microsoft autogen framework, set up or configure autogen to build AI systems, design and implement custom agents and chat bots. Uh we'll be talking about task like coding, reasoning and decision making, build and deploy real world multi- aents workflow that automates complex end toend task. Right? So here we are only not focusing on building, we also focusing on doing the deployment. Right? So overall this course will be having somewhere around 32.5 hours of course and as we go ahead there are some more projects that needs to be uh included. So first of all we go ahead with Python. Python is the prerequisites that you definitely require. Then you have paidentic. Then we start with entire autogen. And if you keep on expan expanding right there are projects, they are use cases. There are good things. There are techniques like how to probably add human in the human in the loop feedback. How to probably go ahead and create a single agent. How to go go ahead and create a multi-a communicate with the other agent. You know how to make sure to uh do this collaboration of multi- agent in autogen. All this specific thing is done. Not only that, we also talk about performance metrics. We talk about uh you know uh building and configuring configuring the autogen agent itself. We have also shown you how to go ahead and use the autogen studio. So there are a whole the whole set of topics that has been discussed with respect to this and super super excited to launch this particular course. Now there is one more announcement that whoever is from my krishnag.in in batch uh in the live classes I hope you have taken this agentic AI right so if you are from this specific batch or agentic 1.0 O batch don't worry you don't need to probably take this particular course because this course will be provided completely for free for everyone out there you know uh and this is the pattern that we follow whoever is the part of our live batches we usually provide them free courses uh from the Udemy so that they get the live access okay uh along with this I would suggest go ahead and try it out each and everything over here right um the prerequisite for this is that you need to have some amount of Python programming lang language knowledge even though if you don't have I have already provided it. You should know how to write modular coding. You should have some understanding of LM models, generative AI models and all. Uh less than all the things you know we have explained things in a much more better way. Each and every topics that you will be specifically seeing over here will be crisps and detail. The kind of materials resources that we have specifically used uh and everything is available for lifetime at just a price of 399. This offer just stays for 2 days. So, go ahead and utilize this opportunity. And yes, this was it from my side. I hope you like this particular video. I'll see you all in the next video. Thank you. Have a great day. Bye-bye.",
}

json_dir = os.path.join(os.getcwd(), "storage", "json")
evaluate(json_dir=json_dir, references=references)
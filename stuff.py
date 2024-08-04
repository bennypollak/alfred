import json

with open('interactionModels/custom/en-US.json') as f:
    configs = json.load(f)
with open('allintents.txt', 'w') as f:
    for intents in configs['interactionModel']['languageModel']['intents']:
        name = intents['name']
        f.write(name+'\n')
        for sample in intents['samples']:
            f.write('   '+sample+'\n')
pass
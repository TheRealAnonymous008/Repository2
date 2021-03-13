#include <iostream>
#include "Nodes.h"
#include "Signal.h"
#include "Port.h"
#include "Clock.h"

int main()
{
    int n = 1;
    int inputs  = 2 * n;
    int outputs = n;

    INPUTNode* inNode = new INPUTNode(inputs);
    OUTPUTNode* outNode = new OUTPUTNode(outputs);
    AbstractNode* node = new DLATCHNode();



    for(int i = 0; i < inputs; i ++){
        inNode->getOutputPort(i)->connectTo(node->getInputPort(i));
        inNode->getOutputPort(i)->connectTo(node->getInputPort(i));
    }

    for(int i = 0; i < outputs; i ++){
        node->getOutputPort(i)->connectTo(outNode->getInputPort(i));
    }

    while(true){
        int first[n] = {1};
        int second[n] = {1};
        std::cin>>first[0]>>second[0];

        for(int i = 0; i < n; i++){
            inNode->setSignalAtPort(new Signal(first[i]), i);
            inNode->setSignalAtPort(new Signal(second[i]), n + i);
        }

        inNode->performOperation();
        node->performOperation();
        outNode->performOperation();

        for(int i = 0; i < n; i++){
            outNode->displaySignalAtPort(i);
            std::cout<<"\n";
        }

    }

    return 0;
}

#include <iostream>
#include "Nodes.h"
#include "Signal.h"
#include "Port.h"
#include "Clock.h"

int main()
{
    // Demonstration of basic synchronous memory storage.
    int n = 1;
    int inputs  = 3;
    int outputs = 1;

    INPUTNode* inNode = new INPUTNode(inputs);
    OUTPUTNode* outNode = new OUTPUTNode(outputs);
    AbstractNode* node = new REGNode();
    Clock* clock = new Clock();



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
        int s = clock->getSignal();
        std::cin>>first[0]>>second[0];
        Signal* clockSignal = new Signal(s);

        inNode->setSignalAtPort(new Signal(first[0]), 0);
        inNode->setSignalAtPort(new Signal(second[0]), 1);

        inNode->setSignalAtPort(clockSignal, 2);

        inNode->performOperation();
        node->performOperation();
        outNode->performOperation();

        for(int i = 0; i < n; i++){
            std::cout<<"Output: ";
            outNode->displaySignalAtPort(i);
            std::cout<<"\nClock signal: "<<clockSignal->getValue()<<"\n";
        }

    }

    return 0;
}

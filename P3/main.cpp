#include <iostream>
#include "Nodes.h"
#include "Signal.h"
#include "Port.h"
#include "Clock.h"
#include <math.h>

int main()
{
    // Demonstration of basic synchronous memory storage.
    int n = 4;
    int k = 4;
    int inputs  = k * n+ (int) log2(k);
    int outputs = n;

    INPUTNode* inNode = new INPUTNode(inputs);
    OUTPUTNode* outNode = new OUTPUTNode(outputs);
    AbstractNode* node = new MUXNode(n, k);
    Clock* clock = new Clock();



    for(int i = 0; i < inputs; i ++){
        inNode->getOutputPort(i)->connectTo(node->getInputPort(i));
    }

    for(int i = 0; i < outputs; i ++){
        node->getOutputPort(i)->connectTo(outNode->getInputPort(i));
    }

    int vals[inputs] = {0, 0, 0, 1,
                        0, 1, 1, 0,
                        1, 0, 1, 1,
                        1, 1, 1, 1,
                        0, 1};

    for(int i = 0; i < inputs; i ++){
        inNode->setSignalAtPort(new Signal(vals[i]), i);
    }

    inNode->performOperation();
    node->performOperation();
    outNode->performOperation();

    for(int i = 0; i < n; i++){
        outNode->displaySignalAtPort(i);
    }


    return 0;
}

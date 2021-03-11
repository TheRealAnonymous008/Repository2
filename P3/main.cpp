#include <iostream>
#include "Nodes.h"
#include "Signal.h"
#include "Port.h"

int main()
{
    INPUTNode inNode(2);
    OUTPUTNode outNode(2);

    inNode.setSignalAtPort(new Signal(1), 0);
    inNode.setSignalAtPort(new Signal(1), 1);

    ADDERNode node;

    inNode.getOutputPort(0)->connectTo(node.getInputPort(0));
    inNode.getOutputPort(1)->connectTo(node.getInputPort(1));
    node.getOutputPort(0)->connectTo(outNode.getInputPort(0));
    node.getOutputPort(1)->connectTo(outNode.getInputPort(1));


    inNode.performOperation();
    node.performOperation();
    outNode.performOperation();

    outNode.displaySignalAtPort(0);
    outNode.displaySignalAtPort(1);

    return 0;
}

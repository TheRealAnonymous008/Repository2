#include "NANDNode.h"

NANDNode::NANDNode() : AbstractNode {"NAND", 2, 1}
{
    //ctor
}

NANDNode::~NANDNode()
{
    //dtor
}

NANDNode::NANDNode(const NANDNode& other)
{
    //copy ctor
}

NANDNode& NANDNode::operator=(const NANDNode& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}

void NANDNode::Process(){
    Port *p1 = this->getInputPort(0);
    Port *p2 = this->getInputPort(1);

    Signal output;
    if(p1->getActualValue().getValue() != 0 && p2->getActualValue().getValue() != 0)
        output = Signal(0);
    else
        output = Signal(1);

    Port* o1 = this->getOutputPort(0);
    o1->setRegister(output);
    o1->receiveData();
}

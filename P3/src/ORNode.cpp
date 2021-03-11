#include "ORNode.h"
#include "Nodes.h"

ORNode::ORNode() : AbstractNode{"OR" ,2, 1}
{
    this->internalNodes.push_back(new NOTNode());
    this->internalNodes.push_back(new NOTNode());
    this->internalNodes.push_back(new NANDNode());

    this->getInputPort(0)->connectTo(this->internalNodes[0]->getInputPort(0));
    this->getInputPort(1)->connectTo(this->internalNodes[1]->getInputPort(0));
    this->internalNodes[0]->getOutputPort(0)->connectTo(this->internalNodes[2]->getInputPort(0));
    this->internalNodes[1]->getOutputPort(0)->connectTo(this->internalNodes[2]->getInputPort(1));
    this->internalNodes[2]->getOutputPort(0)->connectTo(this->getOutputPort(0));
}

ORNode::~ORNode()
{
    //dtor
}

ORNode::ORNode(const ORNode& other)
{
    //copy ctor
}

ORNode& ORNode::operator=(const ORNode& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}

void ORNode::Process(){
    Port* i0 = this->getInputPort(0);
    Port* i1 = this->getInputPort(1);
    Port* out = this->getOutputPort(0);

    i0->sendData();
    i1->sendData();

    this->internalNodes[0]->performOperation();
    this->internalNodes[1]->performOperation();
    this->internalNodes[2]->performOperation();

    out->receiveData();
}

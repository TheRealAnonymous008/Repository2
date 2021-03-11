#include "NOTNode.h"
#include "Nodes.h"

NOTNode::NOTNode() : AbstractNode("NOT", 1, 1)
{
    NANDNode* nandNode = new NANDNode();
    this->internalNodes.push_back(nandNode);
    this->getInputPort(0)->connectTo(nandNode->getInputPort(0));
    nandNode->getOutputPort(0)->connectTo(this->getOutputPort(0));
}

NOTNode::~NOTNode()
{
    //dtor
}

NOTNode::NOTNode(const NOTNode& other)
{
    //copy ctor
}

NOTNode& NOTNode::operator=(const NOTNode& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}

void NOTNode::Process()
{
    Port* in0 = this->getInputPort(0);
    Port* out0 = this->getOutputPort(0);
    AbstractNode* node = this->internalNodes[0];

    in0->sendData();
    node->getInputPort(1)->setRegister(*(new Signal(1)));
    node->getInputPort(1)->receiveData();


    node->performOperation();
    out0->receiveData();
}

#include "ANDNode.h"
#include "Nodes.h"

ANDNode::ANDNode() : AbstractNode {"AND", 2, 1}
{
    this->internalNodes.push_back(new NANDNode());
    this->internalNodes.push_back(new NOTNode());

    this->getInputPort(0)->connectTo(this->internalNodes[0]->getInputPort(0));
    this->getInputPort(1)->connectTo(this->internalNodes[0]->getInputPort(1));
    this->internalNodes[0]->getOutputPort(0)->connectTo(this->internalNodes[1]->getInputPort(0));
    this->internalNodes[1]->getOutputPort(0)->connectTo(this->getOutputPort(0));
}

ANDNode::~ANDNode()
{
    //dtor
}

ANDNode::ANDNode(const ANDNode& other)
{
    //copy ctor
}

ANDNode& ANDNode::operator=(const ANDNode& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}

void ANDNode::Process(){
    Port* i0 = this->getInputPort(0);
    Port* i1 = this->getInputPort(1);
    Port* out = this->getOutputPort(0);
    AbstractNode *nand = this->internalNodes[0];
    AbstractNode *notNode = this->internalNodes[1];

    i0->sendData();
    i1->sendData();

    nand->performOperation();
    notNode->performOperation();
    out->receiveData();

}

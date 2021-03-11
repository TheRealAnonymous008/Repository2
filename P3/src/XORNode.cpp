#include "XORNode.h"
#include "Nodes.h"

XORNode::XORNode() : AbstractNode("XOR" , 2, 1)
{
    this->internalNodes.push_back(new NOTNode);
    this->internalNodes.push_back(new ANDNode);
    this->internalNodes.push_back(new NOTNode);
    this->internalNodes.push_back(new ANDNode);
    this->internalNodes.push_back(new ORNode);

    this->getInputPort(0)->connectTo(this->internalNodes[0]->getInputPort(0));
    this->getInputPort(1)->connectTo(this->internalNodes[2]->getInputPort(0));

    this->internalNodes[0]->getOutputPort(0)->connectTo(this->internalNodes[1]->getInputPort(0));
    this->getInputPort(1)->connectTo(this->internalNodes[1]->getInputPort(1));

    this->internalNodes[2]->getOutputPort(0)->connectTo(this->internalNodes[3]->getInputPort(0));
    this->getInputPort(0)->connectTo(this->internalNodes[3]->getInputPort(1));

    this->internalNodes[1]->getOutputPort(0)->connectTo(this->internalNodes[4]->getInputPort(0));
    this->internalNodes[3]->getOutputPort(0)->connectTo(this->internalNodes[4]->getInputPort(1));

    this->internalNodes[4]->getOutputPort(0)->connectTo(this->getOutputPort(0));

}

XORNode::~XORNode()
{
    //dtor
}

XORNode::XORNode(const XORNode& other)
{
    //copy ctor
}

XORNode& XORNode::operator=(const XORNode& rhs)
{

    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}

void XORNode::Process(){
    Port* i0 = this->getInputPort(0);
    Port* i1 = this->getInputPort(1);
    Port* out = this->getOutputPort(0);

    i0->sendData();
    i1->sendData();


    for(int i = 0; i < 5; i++){
        this->internalNodes[i]->performOperation();
    }

    out->receiveData();

}

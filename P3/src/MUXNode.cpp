#include "MUXNode.h"
#include "Nodes.h"

MUXNode::MUXNode() : AbstractNode(3, 1)
{
    this->internalNodes.push_back(new ANDNode);
    this->internalNodes.push_back(new NOTNode);
    this->internalNodes.push_back(new ANDNode);
    this->internalNodes.push_back(new ORNode);

    this->getInputPort(2)->connectTo(this->internalNodes[0]->getInputPort(0));
    this->getInputPort(0)->connectTo(this->internalNodes[0]->getInputPort(1));

    this->getInputPort(2)->connectTo(this->internalNodes[1]->getInputPort(0));
    this->internalNodes[1]->getOutputPort(0)->connectTo(this->internalNodes[2]->getInputPort(0));
    this->getInputPort(1)->connectTo(this->internalNodes[2]->getInputPort(1));

    this->internalNodes[0]->getOutputPort(0)->connectTo(this->internalNodes[3]->getInputPort(0));
    this->internalNodes[2]->getOutputPort(0)->connectTo(this->internalNodes[3]->getInputPort(1));

    this->internalNodes[3]->getOutputPort(0)->connectTo(this->getOutputPort(0));

}

MUXNode::~MUXNode()
{
    //dtor
}

MUXNode::MUXNode(const MUXNode& other)
{
    //copy ctor
}

MUXNode& MUXNode::operator=(const MUXNode& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}
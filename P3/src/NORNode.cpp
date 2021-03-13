#include "NORNode.h"
#include "Nodes.h"

NORNode::NORNode() : AbstractNode {"NOR", 2, 1}
{
    this->internalNodes.push_back(new ORNode());
    this->internalNodes.push_back(new NOTNode());

    this->getInputPort(0)->connectTo(this->internalNodes[0]->getInputPort(0));
    this->getInputPort(1)->connectTo(this->internalNodes[0]->getInputPort(1));
    this->internalNodes[0]->getOutputPort(0)->connectTo(this->internalNodes[1]->getInputPort(0));
    this->internalNodes[1]->getOutputPort(0)->connectTo(this->getOutputPort(0));
}

NORNode::NORNode(int n) : AbstractNode {"MB_NOR", 2 * n, n}{
    // Multibit NOR
    for(int i = 0; i < n; i ++){
        this->internalNodes.push_back(new NORNode());
        this->getInputPort(i)->connectTo(this->internalNodes[i]->getInputPort(0));
        this->getInputPort(i + n)->connectTo(this->internalNodes[i]->getInputPort(1));
        this->internalNodes[i]->getOutputPort(0)->connectTo(this->getOutputPort(i));
    }
}

NORNode::~NORNode()
{
    //dtor
}

NORNode::NORNode(const NORNode& other)
{
    //copy ctor
}

NORNode& NORNode::operator=(const NORNode& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}

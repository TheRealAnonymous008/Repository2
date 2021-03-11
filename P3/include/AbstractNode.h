#ifndef ABSTRACTNODE_H
#define ABSTRACTNODE_H
#include "Signal.h"
#include "Port.h"

#include<vector>
#include<string>

class AbstractNode
{
    public:
        AbstractNode();
        AbstractNode(int inputs, int outputs);
        AbstractNode(std::string nodeName, int inputs, int outputs);
        virtual ~AbstractNode();
        AbstractNode(const AbstractNode& other);
        AbstractNode& operator=(const AbstractNode& other);

        std::string getId();
        Port* getInputPort(int number);
        Port* getOutputPort(int number);

        void performOperation();


    protected:
        virtual void Process(){};

        std::string id = "";
        int inputPorts = 0;
        int outputPorts = 0;

        std::vector<Port*> inPorts;
        std::vector<Port*> outPorts;
        std::vector<AbstractNode*> internalNodes;

    private:
        std::string generateId();

};

#endif // ABSTRACTNODE_H

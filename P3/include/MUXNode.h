#ifndef MUXNODE_H
#define MUXNODE_H

#include <AbstractNode.h>


class MUXNode : public AbstractNode
{
    public:
        MUXNode();
        virtual ~MUXNode();
        MUXNode(const MUXNode& other);
        MUXNode& operator=(const MUXNode& other);

    private:
        void Process() override;
};

#endif // MUXNODE_H
